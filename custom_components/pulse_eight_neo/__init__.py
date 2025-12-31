from .const import DOMAIN
from .neo_api import NeoMatrix

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = NeoMatrix(entry.data["host"])
    await hass.config_entries.async_forward_entry_setups(entry, ["select"])
    return True
