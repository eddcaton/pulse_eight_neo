from homeassistant import config_entries
import voluptuous as vol
from .const import *

class NeoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"Pulse-Eight Neo ({user_input[CONF_HOST]})",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_OUTPUTS, default=DEFAULT_OUTPUTS): int
            })
        )
