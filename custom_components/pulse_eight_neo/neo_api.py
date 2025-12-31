import logging
from typing import Optional, Tuple

from aiohttp import ClientSession, ClientTimeout

_LOGGER = logging.getLogger(__name__)

class NeoMatrix:
    """
    Pulse-Eight Neo HTTP API (as confirmed by user):
      http://<host>/Port/Set/<INPUT>/<OUTPUT>

    Where INPUT and OUTPUT are zero-indexed.
    Example:
      /Port/Set/0/3  => input 1 to output 4
    """

    def __init__(self, host: str, session: ClientSession):
        self.host = host
        self.session = session

    async def route(self, output_1based: int, input_1based: int) -> Tuple[Optional[int], str]:
        # Convert to zero-based for Neo API
        out0 = int(output_1based) - 1
        in0 = int(input_1based) - 1

        path = f"/Port/Set/{in0}/{out0}"
        url = f"http://{self.host}{path}"

        headers = {
            "Host": self.host,
            "Connection": "close",
            "User-Agent": "HomeAssistant-PulseEightNeo/2.1.0",
            "Accept": "*/*",
        }

        _LOGGER.warning("Neo request -> %s", url)

        try:
            timeout = ClientTimeout(total=4)
            async with self.session.get(url, headers=headers, timeout=timeout) as resp:
                body = await resp.text(errors="ignore")
                _LOGGER.warning("Neo response <- %s (%s bytes)", resp.status, len(body))
                if body:
                    # Log only first 200 chars to avoid spam
                    _LOGGER.debug("Neo body (first 200): %s", body[:200])
                return resp.status, body
        except Exception as e:
            _LOGGER.error("Neo HTTP error talking to %s: %s", self.host, e)
            return None, str(e)
