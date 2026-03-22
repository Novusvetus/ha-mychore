"""Data handling for ha-mychore integration."""

from datetime import datetime
from homeassistant.helpers.storage import Store

class ChoreData:
    """Class to handle chore data and persistence."""

    def __init__(self, hass, entry_id):
        """Initialize ChoreData."""
        self.hass = hass
        self.entry_id = entry_id
        self.store = Store(hass, "ha-mychore", f"{entry_id}.json")
        self.last_done = None
        self.due_today = False
        self._listeners = []
        self._loaded = False

    async def async_load(self):
        """Load data from storage."""
        data = await self.store.async_load()
        if data:
            last_done_str = data.get("last_done")
            self.last_done = (
                datetime.fromisoformat(last_done_str) if last_done_str else None
            )
        self._loaded = True

    async def async_save(self):
        """Save data to storage."""
        data = {
            "last_done": self.last_done.isoformat() if self.last_done else None
        }
        await self.store.async_save(data)

    def set_last_done(self, dt):
        """Set the last done timestamp."""
        self.last_done = dt
        # Schedule save
        self.hass.async_create_task(self.async_save())
        for listener in self._listeners:
            listener()

    def set_due_today(self, value):
        """Set the due_today flag."""
        self.due_today = value
        for listener in self._listeners:
            listener()

    def add_listener(self, listener):
        """Add a listener for data changes."""
        self._listeners.append(listener)

async def get_chore_data(hass, config_entry, domain):
    """Get or create ChoreData for the entry."""
    entry_id = config_entry.entry_id
    if domain not in hass.data:
        hass.data[domain] = {}
    if entry_id not in hass.data[domain]:
        hass.data[domain][entry_id] = ChoreData(hass, entry_id)
        await hass.data[domain][entry_id].async_load()
    return hass.data[domain][entry_id]
