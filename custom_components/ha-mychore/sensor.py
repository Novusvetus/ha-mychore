"""Sensor platform for ha-mychore integration."""

from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN
from .data import get_chore_data

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
) -> None:
    """Set up the sensor platform (not used with config_flow)."""
    # This is for YAML config, but since we have config_flow, maybe not needed
    pass

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    chore_data = await get_chore_data(hass, config_entry, DOMAIN)
    sensor = ChoreSensor(chore_data, config_entry)
    async_add_entities([sensor])

class ChoreSensor(SensorEntity):
    """Sensor entity for showing chore overdue percentage."""

    def __init__(self, chore_data, config_entry):
        """Initialize the sensor."""
        self.chore_data = chore_data
        self.config_entry = config_entry
        self._name = config_entry.data["name"]
        self._points = config_entry.data["points"]
        self._interval_hours = config_entry.data["interval_hours"]
        self.chore_data.add_listener(self.async_write_ha_state)
        self._attr_translation_key = "chore_percentage"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return f"{self.config_entry.entry_id}_sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.chore_data.last_done is None:
            return 100
        now = datetime.now()
        elapsed = now - self.chore_data.last_done
        total = timedelta(hours=self._interval_hours)
        percentage = max(0, (elapsed / total) * 100)
        return round(percentage, 2)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "%"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "last_done": self.chore_data.last_done.isoformat() if self.chore_data.last_done else None,
            "points": self._points,
            "interval_hours": self._interval_hours,
            "due_today": self.chore_data.due_today,
        }
