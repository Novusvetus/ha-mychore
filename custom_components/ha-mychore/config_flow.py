import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

class MyChoreConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): cv.string,
                vol.Required("points", default=1): cv.positive_int,
                vol.Required("interval_hours", default=24): cv.positive_int,
            }),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MyChoreOptionsFlow(config_entry)

class MyChoreOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("points", default=self.config_entry.data.get("points", 1)): cv.positive_int,
                vol.Required("interval_hours", default=self.config_entry.data.get("interval_hours", 24)): cv.positive_int,
            }),
        )
