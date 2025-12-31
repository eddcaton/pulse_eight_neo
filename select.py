from homeassistant.components.select import SelectEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    outputs = entry.data["outputs"]
    api = hass.data[DOMAIN]

    async_add_entities([
        NeoOutputSelect(api, o+1) for o in range(outputs)
    ])

class NeoOutputSelect(SelectEntity):
    def __init__(self, api, output):
        self.api = api
        self._output = output
        self._attr_name = f"Neo Output {output}"
        self._attr_options = [f"Input {i}" for i in range(1,7)]
        self._attr_current_option = "Input 1"

    async def async_select_option(self, option):
        input_num = option.split(" ")[1]
        self.api.route(self._output, input_num)
        self._attr_current_option = option
        self.async_write_ha_state()
