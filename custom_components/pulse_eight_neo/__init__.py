from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .neo_api import NeoMatrix

PLATFORMS = ["select"]

async def async_setup_entry(hass, entry):
    host = entry.data["host"]
    session = async_get_clientsession(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = NeoMatrix(host, session)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
