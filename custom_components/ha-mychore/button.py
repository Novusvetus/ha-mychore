from datetime import datetime
from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .data import ChoreData

async def async_setup_entry(hass, config_entry, async_add_entities):
    entry_id = config_entry.entry_id
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if entry_id not in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry_id] = ChoreData(hass, entry_id)
        await hass.data[DOMAIN][entry_id].async_load()
    chore_data = hass.data[DOMAIN][entry_id]
    button = ChoreButton(chore_data, config_entry)
    async_add_entities([button])

class ChoreButton(ButtonEntity):
    def __init__(self, chore_data, config_entry):
        self.chore_data = chore_data
        self.config_entry = config_entry
        self._name = config_entry.data["name"]
        self._attr_translation_key = "chore_button"

    @property
    def name(self):
        return f"{self._name} Button"

    @property
    def unique_id(self):
        return f"{self.config_entry.entry_id}_button"

    async def async_press(self) -> None:
        self.chore_data.set_last_done(datetime.now())
        # To update the sensor, we can find it and call async_write_ha_state
        # But since it's the same hass, perhaps trigger a state update
        # For simplicity, since the sensor state changes over time, it will update eventually
        # But to force, we can use hass.bus.async_fire or something, but let's add a method to sensor
        # Since ChoreData is shared, and sensor has async_write_ha_state, but no reference
        # Perhaps make ChoreData have a callback
        # For now, let's assume the sensor updates on its own, or add a timer

# To make it update immediately, let's add a method to ChoreSensor to update

# But since no reference, perhaps use hass.states.async_set or something, but better to have the sensor listen to a signal.

# Simple way: in ChoreData, have a list of entities to update

# Let's modify ChoreData

# In data.py:

class ChoreData:
    def __init__(self):
        self.last_done = None
        self._listeners = []

    def set_last_done(self, dt):
        self.last_done = dt
        for listener in self._listeners:
            listener()

    def add_listener(self, listener):
        self._listeners.append(listener)

# Then in ChoreSensor __init__:

self.chore_data.add_listener(self.async_write_ha_state)

# Yes!

# Update data.py
