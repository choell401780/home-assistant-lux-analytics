"""Config flow for Lux Analytics."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_BRIGHT_THRESHOLD,
    CONF_SENSOR_LABEL,
    CONF_SOURCE_SENSOR,
    CONF_UPDATE_INTERVAL,
    DEFAULT_BRIGHT_THRESHOLD,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    build_entity_id,
)
from .coordinator import discover_illuminance_sensors


class LuxAnalyticsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle initial configuration: pick one source sensor + optional label."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        discovered = discover_illuminance_sensors(self.hass)
        errors: dict[str, str] = {}

        if user_input is not None:
            source = user_input[CONF_SOURCE_SENSOR]
            label = user_input.get(CONF_SENSOR_LABEL, "").strip()

            # Prevent duplicate entries for the same source sensor
            await self.async_set_unique_id(f"{DOMAIN}_{source}")
            self._abort_if_unique_id_configured()

            title = f"Lux Analytics – {label}" if label else f"Lux Analytics ({source.split('.')[-1]})"

            return self.async_create_entry(
                title=title,
                data={
                    CONF_SOURCE_SENSOR: source,
                    CONF_SENSOR_LABEL: label,
                    CONF_BRIGHT_THRESHOLD: user_input.get(CONF_BRIGHT_THRESHOLD, DEFAULT_BRIGHT_THRESHOLD),
                    CONF_UPDATE_INTERVAL: user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
                },
            )

        sensor_options = [
            selector.SelectOptionDict(value=s, label=s) for s in discovered
        ]

        schema = vol.Schema(
            {
                vol.Required(CONF_SOURCE_SENSOR): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=sensor_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        custom_value=True,
                    )
                ),
                vol.Optional(CONF_SENSOR_LABEL, default=""): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
                ),
                vol.Optional(CONF_BRIGHT_THRESHOLD, default=DEFAULT_BRIGHT_THRESHOLD): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=200000, step=100, mode=selector.NumberSelectorMode.BOX)
                ),
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=60, max=3600, step=60, mode=selector.NumberSelectorMode.BOX)
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "discovered": str(len(discovered)),
                "example_id": build_entity_id("current"),
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return LuxAnalyticsOptionsFlow(config_entry)


class LuxAnalyticsOptionsFlow(config_entries.OptionsFlow):
    """Reconfigure thresholds and interval (source sensor is read-only)."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_threshold = self.config_entry.options.get(
            CONF_BRIGHT_THRESHOLD,
            self.config_entry.data.get(CONF_BRIGHT_THRESHOLD, DEFAULT_BRIGHT_THRESHOLD),
        )
        current_interval = self.config_entry.options.get(
            CONF_UPDATE_INTERVAL,
            self.config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
        )

        schema = vol.Schema(
            {
                vol.Optional(CONF_BRIGHT_THRESHOLD, default=current_threshold): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=200000, step=100, mode=selector.NumberSelectorMode.BOX)
                ),
                vol.Optional(CONF_UPDATE_INTERVAL, default=current_interval): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=60, max=3600, step=60, mode=selector.NumberSelectorMode.BOX)
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
