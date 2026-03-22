"""Button platform for ha-mychore integration."""

from datetime import datetime
from homeassistant.components.button import ButtonEntity

from .const import DOMAIN
from .data import get_chore_data

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the button platform."""
    chore_data = await get_chore_data(hass, config_entry, DOMAIN)
    button = ChoreButton(chore_data, config_entry)
    async_add_entities([button])

class ChoreButton(ButtonEntity):
    """Button entity for marking a chore as done."""

    def __init__(self, chore_data, config_entry):
        """Initialize the button."""
        self.chore_data = chore_data
        self.config_entry = config_entry
        self._name = config_entry.data["name"]
        self._attr_translation_key = "chore_button"

    @property
    def name(self):
        """Return the name of the button."""
        return f"{self._name} Button"

    @property
    def unique_id(self):
        """Return the unique ID of the button."""
        return f"{self.config_entry.entry_id}_button"

    async def async_press(self) -> None:
        """Handle the button press."""
        self.chore_data.set_last_done(datetime.now())
