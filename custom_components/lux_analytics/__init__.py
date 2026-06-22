"""Home Assistant Lux Analytics – Custom Integration."""

from __future__ import annotations

import logging

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
