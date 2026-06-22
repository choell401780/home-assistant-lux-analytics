"""Sensor platform for Lux Analytics."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_SENSOR_LABEL,
    CONF_SOURCE_SENSOR,
    DOMAIN,
    SENSOR_TYPES,
    VERSION,
    build_entity_id,
)
from .coordinator import LuxAnalyticsCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities from a config entry."""
    coordinator: LuxAnalyticsCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    label = config_entry.data.get(CONF_SENSOR_LABEL, "")

    entities = [
        LuxSensorEntity(coordinator, config_entry, sensor_key, label)
        for sensor_key in SENSOR_TYPES
    ]
    async_add_entities(entities, True)


class LuxSensorEntity(CoordinatorEntity[LuxAnalyticsCoordinator], SensorEntity):
    """One statistical sensor derived from the configured source lux sensor.

    entity_id follows a predictable scheme so the bundled dashboard works
    out-of-the-box without any manual editing:
      no label  → sensor.lux_analytics_aktuelle_helligkeit
      label=garten → sensor.lux_analytics_garten_aktuelle_helligkeit
    """

    def __init__(
        self,
        coordinator: LuxAnalyticsCoordinator,
        config_entry: ConfigEntry,
        sensor_key: str,
        label: str,
    ) -> None:
        super().__init__(coordinator)
        stype = SENSOR_TYPES[sensor_key]
        self._sensor_key = sensor_key
        source = coordinator.source_entity_id

        # Stable unique_id: entry_id never changes even if user renames source sensor
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_key}"

        display_label = f" [{label}]" if label else ""
        self._attr_name = f"{stype['name']}{display_label}"
        self._attr_icon = stype["icon"]
        self._attr_native_unit_of_measurement = stype["unit"]

        # Predictable entity_id — set at first registration, then stored in registry
        self.entity_id = build_entity_id(sensor_key, label)

        if stype["unit"] == "lx":
            self._attr_device_class = SensorDeviceClass.ILLUMINANCE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif stype["unit"] == "h":
            self._attr_state_class = SensorStateClass.MEASUREMENT

        device_name = f"Lux Analytics – {label}" if label else f"Lux Analytics ({source.split('.')[-1]})"
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=device_name,
            manufacturer="Home Assistant Lux Analytics",
            model="Lux Statistics",
            sw_version=VERSION,
        )

    @property
    def native_value(self) -> Any:
        return self.coordinator.data.get(self._sensor_key) if self.coordinator.data else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"source_entity": self.coordinator.source_entity_id}
