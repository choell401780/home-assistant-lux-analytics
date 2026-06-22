"""Config flow for Lux Analytics."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_AUTO_DISCOVER,
    CONF_BRIGHT_THRESHOLD,
    CONF_SENSORS,
    CONF_UPDATE_INTERVAL,
    DEFAULT_AUTO_DISCOVER,
    DEFAULT_BRIGHT_THRESHOLD,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)
from .coordinator import LuxAnalyticsCoordinator


class LuxAnalyticsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial configuration."""

    VERSION = 1

    def __init__(self) -> None:
        self._discovered_sensors: list[str] = []

    async def async_step_user(self, user_input=None):
        """First step: auto-discover or pick sensors."""
        temp_coordinator = LuxAnalyticsCoordinator(self.hass, [])
        self._discovered_sensors = temp_coordinator.discover_illuminance_sensors()

        if user_input is not None:
            auto_discover = user_input.get(CONF_AUTO_DISCOVER, DEFAULT_AUTO_DISCOVER)
            if auto_discover:
                sensors = self._discovered_sensors
            else:
                sensors = user_input.get(CONF_SENSORS, [])

            return self.async_create_entry(
                title="Lux Analytics",
                data={
                    CONF_SENSORS: sensors,
                    CONF_AUTO_DISCOVER: auto_discover,
                    CONF_BRIGHT_THRESHOLD: user_input.get(CONF_BRIGHT_THRESHOLD, DEFAULT_BRIGHT_THRESHOLD),
                    CONF_UPDATE_INTERVAL: user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
                },
            )

        sensor_options = [
            selector.SelectOptionDict(value=s, label=s)
            for s in self._discovered_sensors
        ]

        schema = vol.Schema({
            vol.Optional(CONF_AUTO_DISCOVER, default=DEFAULT_AUTO_DISCOVER): bool,
            vol.Optional(CONF_SENSORS, default=[]): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=sensor_options,
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
            vol.Optional(CONF_BRIGHT_THRESHOLD, default=DEFAULT_BRIGHT_THRESHOLD): int,
            vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={
                "discovered": str(len(self._discovered_sensors)),
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return LuxAnalyticsOptionsFlow(config_entry)


class LuxAnalyticsOptionsFlow(config_entries.OptionsFlow):
    """Allow reconfiguration of sensors and thresholds."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        temp_coordinator = LuxAnalyticsCoordinator(self.hass, [])
        discovered = temp_coordinator.discover_illuminance_sensors()
        sensor_options = [
            selector.SelectOptionDict(value=s, label=s) for s in discovered
        ]

        current_sensors = self.config_entry.data.get(CONF_SENSORS, [])
        current_threshold = self.config_entry.data.get(CONF_BRIGHT_THRESHOLD, DEFAULT_BRIGHT_THRESHOLD)
        current_interval = self.config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

        schema = vol.Schema({
            vol.Optional(CONF_SENSORS, default=current_sensors): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=sensor_options,
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
            vol.Optional(CONF_BRIGHT_THRESHOLD, default=current_threshold): int,
            vol.Optional(CONF_UPDATE_INTERVAL, default=current_interval): int,
        })

        return self.async_show_form(step_id="init", data_schema=schema)
