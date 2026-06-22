"""DataUpdateCoordinator for Lux Analytics."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

import aiohttp
from homeassistant.components.recorder import get_instance
from homeassistant.components.recorder.history import get_significant_states
from homeassistant.components.recorder.statistics import statistics_during_period
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    BRIGHTNESS_CLASSES,
    DEFAULT_BRIGHT_THRESHOLD,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    GITHUB_REPO,
    ILLUMINANCE_DEVICE_CLASSES,
    ILLUMINANCE_KEYWORDS,
    ILLUMINANCE_UNITS,
    VERSION,
)

_LOGGER = logging.getLogger(__name__)

GITHUB_RELEASES_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def classify_brightness(lux: float) -> str:
    """Return the brightness class name for a given lux value."""
    for cls in BRIGHTNESS_CLASSES:
        if cls["min"] <= lux < cls["max"]:
            return cls["name"]
    return BRIGHTNESS_CLASSES[-1]["name"]


def calculate_sun_index(lux: float) -> float:
    """Normalize lux value to a 0-100 sun index."""
    max_lux = 100000.0
    return min(round((lux / max_lux) * 100, 1), 100.0)


class LuxAnalyticsCoordinator(DataUpdateCoordinator):
    """Coordinator fetching lux statistics and github version info."""

    def __init__(
        self,
        hass: HomeAssistant,
        sensor_ids: list[str],
        bright_threshold: int = DEFAULT_BRIGHT_THRESHOLD,
        update_interval: int = DEFAULT_UPDATE_INTERVAL,
    ) -> None:
        self.sensor_ids = sensor_ids
        self.bright_threshold = bright_threshold
        self._latest_version: str | None = None
        self._release_notes: str | None = None
        self._version_check_interval = timedelta(hours=6)
        self._last_version_check: datetime | None = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    @property
    def installed_version(self) -> str:
        return VERSION

    @property
    def latest_version(self) -> str | None:
        return self._latest_version

    @property
    def update_available(self) -> bool:
        if self._latest_version is None:
            return False
        return self._latest_version != VERSION

    @property
    def release_notes(self) -> str | None:
        return self._release_notes

    # ------------------------------------------------------------------
    # Sensor discovery
    # ------------------------------------------------------------------

    def discover_illuminance_sensors(self) -> list[str]:
        """Return entity_ids of all illuminance sensors found in HA."""
        found: list[str] = []
        for state in self.hass.states.async_all("sensor"):
            attrs = state.attributes
            device_class = attrs.get("device_class", "")
            unit = attrs.get("unit_of_measurement", "")
            entity_id = state.entity_id

            if device_class in ILLUMINANCE_DEVICE_CLASSES:
                found.append(entity_id)
                continue
            if unit.lower() in ILLUMINANCE_UNITS:
                found.append(entity_id)
                continue
            if any(kw in entity_id.lower() for kw in ILLUMINANCE_KEYWORDS):
                found.append(entity_id)
        return list(dict.fromkeys(found))

    # ------------------------------------------------------------------
    # Main update
    # ------------------------------------------------------------------

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch statistics for all configured sensors."""
        data: dict[str, Any] = {}

        for entity_id in self.sensor_ids:
            try:
                sensor_data = await self._fetch_sensor_data(entity_id)
                data[entity_id] = sensor_data
            except Exception as exc:  # noqa: BLE001
                _LOGGER.warning("Failed to fetch data for %s: %s", entity_id, exc)
                data[entity_id] = self._empty_sensor_data()

        await self._maybe_check_github_version()
        return data

    async def _fetch_sensor_data(self, entity_id: str) -> dict[str, Any]:
        """Build statistics dict for one sensor."""
        now = dt_util.now()
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = day_start - timedelta(days=now.weekday())
        month_start = day_start.replace(day=1)
        h24_start = now - timedelta(hours=24)
        d7_start = now - timedelta(days=7)
        d30_start = now - timedelta(days=30)

        current_lux = self._get_current_lux(entity_id)

        day_vals   = await self._get_history_values(entity_id, day_start, now)
        week_vals  = await self._get_history_values(entity_id, week_start, now)
        month_vals = await self._get_history_values(entity_id, month_start, now)
        h24_vals   = await self._get_history_values(entity_id, h24_start, now)
        d7_vals    = await self._get_history_values(entity_id, d7_start, now)
        d30_vals   = await self._get_history_values(entity_id, d30_start, now)

        trend = self._calculate_trend(h24_vals, current_lux)

        return {
            "current":            current_lux,
            "status":             classify_brightness(current_lux) if current_lux is not None else "Unbekannt",
            "trend":              trend,
            "sun_index":          calculate_sun_index(current_lux) if current_lux is not None else 0.0,
            "day_min":            self._safe_min(day_vals),
            "day_max":            self._safe_max(day_vals),
            "day_avg":            self._safe_avg(day_vals),
            "week_min":           self._safe_min(week_vals),
            "week_max":           self._safe_max(week_vals),
            "week_avg":           self._safe_avg(week_vals),
            "month_min":          self._safe_min(month_vals),
            "month_max":          self._safe_max(month_vals),
            "month_avg":          self._safe_avg(month_vals),
            "bright_hours_day":   self._bright_hours(day_vals, self.bright_threshold),
            "bright_hours_week":  self._bright_hours(week_vals, self.bright_threshold),
            "bright_hours_month": self._bright_hours(month_vals, self.bright_threshold),
            "avg_24h":            self._safe_avg(h24_vals),
            "avg_7d":             self._safe_avg(d7_vals),
            "avg_30d":            self._safe_avg(d30_vals),
        }

    def _get_current_lux(self, entity_id: str) -> float | None:
        state = self.hass.states.get(entity_id)
        if state is None or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN, ""):
            return None
        try:
            return float(state.state)
        except ValueError:
            return None

    async def _get_history_values(
        self, entity_id: str, start: datetime, end: datetime
    ) -> list[float]:
        """Return numeric state values from recorder history."""
        try:
            instance = get_instance(self.hass)
            states = await instance.async_add_executor_job(
                get_significant_states,
                self.hass,
                start,
                end,
                [entity_id],
            )
        except Exception as exc:  # noqa: BLE001
            _LOGGER.debug("History unavailable for %s: %s", entity_id, exc)
            return []

        values: list[float] = []
        for state in states.get(entity_id, []):
            if state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN):
                try:
                    values.append(float(state.state))
                except ValueError:
                    pass
        return values

    # ------------------------------------------------------------------
    # Statistical helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _safe_min(values: list[float]) -> float | None:
        return round(min(values), 1) if values else None

    @staticmethod
    def _safe_max(values: list[float]) -> float | None:
        return round(max(values), 1) if values else None

    @staticmethod
    def _safe_avg(values: list[float]) -> float | None:
        return round(sum(values) / len(values), 1) if values else None

    @staticmethod
    def _bright_hours(values: list[float], threshold: int) -> float:
        """Estimate hours above threshold (assuming ~1 min per sample)."""
        if not values:
            return 0.0
        bright = sum(1 for v in values if v >= threshold)
        return round(bright / 60, 2)

    @staticmethod
    def _calculate_trend(recent_values: list[float], current: float | None) -> str:
        if current is None or len(recent_values) < 10:
            return "Stabil"
        avg = sum(recent_values) / len(recent_values)
        delta = current - avg
        if delta > avg * 0.15:
            return "Steigend"
        if delta < -avg * 0.15:
            return "Fallend"
        return "Stabil"

    @staticmethod
    def _empty_sensor_data() -> dict[str, Any]:
        return {k: None for k in (
            "current", "status", "trend", "sun_index",
            "day_min", "day_max", "day_avg",
            "week_min", "week_max", "week_avg",
            "month_min", "month_max", "month_avg",
            "bright_hours_day", "bright_hours_week", "bright_hours_month",
            "avg_24h", "avg_7d", "avg_30d",
        )}

    # ------------------------------------------------------------------
    # GitHub version check
    # ------------------------------------------------------------------

    async def _maybe_check_github_version(self) -> None:
        now = dt_util.now()
        if (
            self._last_version_check is not None
            and now - self._last_version_check < self._version_check_interval
        ):
            return
        self._last_version_check = now
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    GITHUB_RELEASES_URL, timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        payload = await resp.json()
                        tag = payload.get("tag_name", "").lstrip("v")
                        self._latest_version = tag or None
                        self._release_notes = payload.get("body", "")
        except Exception as exc:  # noqa: BLE001
            _LOGGER.debug("GitHub version check failed: %s", exc)
