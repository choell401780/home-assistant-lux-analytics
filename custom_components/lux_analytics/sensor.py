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

from .const import DOMAIN, SENSOR_TYPES, VERSION
from .coordinator import LuxAnalyticsCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities from a config entry."""
    coordinator: LuxAnalyticsCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[LuxSensorEntity] = []
    for source_entity_id in coordinator.sensor_ids:
        safe_id = source_entity_id.replace(".", "_")
        for sensor_key in SENSOR_TYPES:
            entities.append(
                LuxSensorEntity(coordinator, config_entry, source_entity_id, safe_id, sensor_key)
            )

    async_add_entities(entities, True)


class LuxSensorEntity(CoordinatorEntity[LuxAnalyticsCoordinator], SensorEntity):
    """A single statistical sensor derived from a source lux sensor."""

    def __init__(
        self,
        coordinator: LuxAnalyticsCoordinator,
        config_entry: ConfigEntry,
        source_entity_id: str,
        safe_id: str,
        sensor_key: str,
    ) -> None:
        super().__init__(coordinator)
        self._source_entity_id = source_entity_id
        self._sensor_key = sensor_key
        stype = SENSOR_TYPES[sensor_key]

        self._attr_unique_id = f"{config_entry.entry_id}_{safe_id}_{sensor_key}"
        self._attr_name = f"{source_entity_id} {stype['name']}"
        self._attr_icon = stype["icon"]
        self._attr_native_unit_of_measurement = stype["unit"]

        if stype["unit"] == "lx":
            self._attr_device_class = SensorDeviceClass.ILLUMINANCE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif stype["unit"] == "h":
            self._attr_state_class = SensorStateClass.MEASUREMENT

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"{config_entry.entry_id}_{safe_id}")},
            name=f"Lux Analytics – {source_entity_id}",
            manufacturer="Home Assistant Lux Analytics",
            model="Lux Statistics",
            sw_version=VERSION,
        )

    @property
    def native_value(self) -> Any:
        sensor_data = self.coordinator.data.get(self._source_entity_id, {})
        return sensor_data.get(self._sensor_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"source_entity": self._source_entity_id}
