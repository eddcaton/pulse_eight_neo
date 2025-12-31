from homeassistant.components.select import SelectEntity

from .const import DOMAIN, DEFAULT_INPUTS

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    outputs = int(entry.data["outputs"])

    entities = [NeoOutputSelect(api, output=i) for i in range(1, outputs + 1)]
    async_add_entities(entities)

class NeoOutputSelect(SelectEntity):
    def __init__(self, api, output: int):
        self.api = api
        self._output = output
        self._attr_name = f"Neo Output {output}"
        self._attr_unique_id = f"pulse_eight_neo_output_{output}"
        self._attr_options = [f"Input {i}" for i in range(1, DEFAULT_INPUTS + 1)]
        self._attr_current_option = "Input 1"

    async def async_select_option(self, option: str) -> None:
        input_num = int(option.split(" ")[1])

        status, body = await self.api.route(output_1based=self._output, input_1based=input_num)

        # Update UI state regardless; if status is None, logs will show why
        self._attr_current_option = option
        self.async_write_ha_state()
