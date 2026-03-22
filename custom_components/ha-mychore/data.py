from datetime import datetime
from homeassistant.helpers.storage import Store

class ChoreData:
    def __init__(self, hass, entry_id):
        self.hass = hass
        self.entry_id = entry_id
        self.store = Store(hass, "ha-mychore", f"{entry_id}.json")
        self.last_done = None
        self.due_today = False
        self._listeners = []
        self._loaded = False

    async def async_load(self):
        data = await self.store.async_load()
        if data:
            self.last_done = datetime.fromisoformat(data.get("last_done")) if data.get("last_done") else None
        self._loaded = True

    async def async_save(self):
        data = {"last_done": self.last_done.isoformat() if self.last_done else None}
        await self.store.async_save(data)

    def set_last_done(self, dt):
        self.last_done = dt
        # Schedule save
        self.hass.async_create_task(self.async_save())
        for listener in self._listeners:
            listener()

    def set_due_today(self, value):
        self.due_today = value
        for listener in self._listeners:
            listener()

    def add_listener(self, listener):
        self._listeners.append(listener)

async def get_chore_data(hass, config_entry, domain):
    entry_id = config_entry.entry_id
    if domain not in hass.data:
        hass.data[domain] = {}
    if entry_id not in hass.data[domain]:
        hass.data[domain][entry_id] = ChoreData(hass, entry_id)
        await hass.data[domain][entry_id].async_load()
    return hass.data[domain][entry_id]
