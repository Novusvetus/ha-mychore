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
