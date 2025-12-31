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

    async def handle_power_on(call):
        await hass.data[DOMAIN][entry.entry_id].power_on(call.data["output"])

    async def handle_power_off(call):
        await hass.data[DOMAIN][entry.entry_id].power_off(call.data["output"])

    hass.services.async_register(DOMAIN, "power_on", handle_power_on)
    hass.services.async_register(DOMAIN, "power_off", handle_power_off)

    return True
