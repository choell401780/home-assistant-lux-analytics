"""Home Assistant Lux Analytics – Custom Integration."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_BRIGHT_THRESHOLD,
    CONF_SOURCE_SENSOR,
    CONF_UPDATE_INTERVAL,
    DEFAULT_BRIGHT_THRESHOLD,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)
from .coordinator import LuxAnalyticsCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]

_CARD_URL = "/lux-analytics/lux-analytics-card.js"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register the JS card as a static file and Lovelace resource."""
    hass.http.register_static_path(
        "/lux-analytics",
        str(Path(__file__).parent / "www"),
        cache_headers=False,
    )

    async def _register_resource(event=None) -> None:
        try:
            lovelace = hass.data.get("lovelace")
            if lovelace is None:
                _LOGGER.debug("Lux Analytics: lovelace not in hass.data, skipping resource registration")
                return

            resources = (
                lovelace.get("resources")
                if isinstance(lovelace, dict)
                else getattr(lovelace, "resources", None)
            )
            if resources is None:
                _LOGGER.debug("Lux Analytics: Lovelace resources unavailable (YAML mode?)")
                return

            for item in resources.async_items():
                if item.get("url") == _CARD_URL:
                    return  # already registered

            await resources.async_create_item({"res_type": "module", "url": _CARD_URL})
            _LOGGER.info("Lux Analytics: Lovelace card resource registered (%s)", _CARD_URL)
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Lux Analytics: could not register Lovelace resource: %s", err)

    hass.bus.async_listen_once("homeassistant_started", _register_resource)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lux Analytics from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    source_sensor = entry.data.get(CONF_SOURCE_SENSOR, "")
    bright_threshold = entry.options.get(
        CONF_BRIGHT_THRESHOLD,
        entry.data.get(CONF_BRIGHT_THRESHOLD, DEFAULT_BRIGHT_THRESHOLD),
    )
    update_interval = entry.options.get(
        CONF_UPDATE_INTERVAL,
        entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
    )

    if not source_sensor:
        _LOGGER.error("Lux Analytics: no source sensor configured in entry %s", entry.entry_id)
        return False

    coordinator = LuxAnalyticsCoordinator(
        hass,
        source_entity_id=source_sensor,
        bright_threshold=bright_threshold,
        update_interval=update_interval,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    _LOGGER.info("Lux Analytics set up for sensor: %s", source_sensor)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
