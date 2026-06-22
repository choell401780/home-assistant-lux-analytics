"""Home Assistant Lux Analytics – Custom Integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_AUTO_DISCOVER,
    CONF_BRIGHT_THRESHOLD,
    CONF_SENSORS,
    CONF_UPDATE_INTERVAL,
    DEFAULT_BRIGHT_THRESHOLD,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)
from .coordinator import LuxAnalyticsCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lux Analytics from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    auto_discover = entry.data.get(CONF_AUTO_DISCOVER, True)
    configured_sensors = entry.data.get(CONF_SENSORS, [])
    bright_threshold = entry.data.get(CONF_BRIGHT_THRESHOLD, DEFAULT_BRIGHT_THRESHOLD)
    update_interval = entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

    coordinator = LuxAnalyticsCoordinator(
        hass,
        sensor_ids=[],
        bright_threshold=bright_threshold,
        update_interval=update_interval,
    )

    if auto_discover:
        sensor_ids = coordinator.discover_illuminance_sensors()
        _LOGGER.info("Lux Analytics auto-discovered %d sensors: %s", len(sensor_ids), sensor_ids)
    else:
        sensor_ids = configured_sensors
        _LOGGER.info("Lux Analytics using %d configured sensors", len(sensor_ids))

    coordinator.sensor_ids = sensor_ids

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

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
