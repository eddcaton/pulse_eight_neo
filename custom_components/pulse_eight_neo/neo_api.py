import logging
from aiohttp import ClientSession, ClientTimeout

_LOGGER = logging.getLogger(__name__)

class NeoMatrix:
    """
    Pulse-Eight Neo HTTP API

    Routing:
        /Port/Set/<INPUT>/<OUTPUT>

    CEC:
        /CEC/On/<OUTPUT>
        /CEC/Off/<OUTPUT>

    All zero indexed.
    """

    def __init__(self, host: str, session: ClientSession):
        self.host = host
        self.session = session
        self.timeout = ClientTimeout(total=4)

    async def _get(self, path):
        url = f"http://{self.host}{path}"
        headers = {
            "Host": self.host,
            "Connection": "close",
            "User-Agent": "HomeAssistant-PulseEightNeo",
            "Accept": "*/*"
        }

        _LOGGER.warning("Neo -> %s", url)

        try:
            async with self.session.get(url, headers=headers, timeout=self.timeout) as resp:
                body = await resp.text(errors="ignore")
                _LOGGER.warning("Neo <- %s (%s bytes)", resp.status, len(body))
                return resp.status, body
        except Exception as e:
            _LOGGER.error("Neo HTTP error: %s", e)
            return None, str(e)

    async def route(self, output_1based: int, input_1based: int):
        out0 = int(output_1based) - 1
        in0 = int(input_1based) - 1
        return await self._get(f"/Port/Set/{in0}/{out0}")

    async def power_on(self, output_1based: int):
        out0 = int(output_1based) - 1
        return await self._get(f"/CEC/On/{out0}")

    async def power_off(self, output_1based: int):
        out0 = int(output_1based) - 1
        return await self._get(f"/CEC/Off/{out0}")
