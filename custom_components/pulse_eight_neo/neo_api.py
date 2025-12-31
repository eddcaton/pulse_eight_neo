import http.client
import logging

_LOGGER = logging.getLogger(__name__)

class NeoMatrix:
    def __init__(self, host):
        self.host = host

    def route(self, output, input):
        # Neo API is zero-indexed and is INPUT first, OUTPUT second
        out = int(output) - 1
        inp = int(input) - 1

        path = f"/Port/Set/{inp}/{out}"
        _LOGGER.warning(f"Neo HTTP -> http://{self.host}{path}")

        try:
            conn = http.client.HTTPConnection(self.host, 80, timeout=3)
            conn.request("GET", path)
            resp = conn.getresponse()
            resp.read()
            conn.close()
            _LOGGER.warning(f"Neo response: {resp.status}")
            return resp.status
        except Exception as e:
            _LOGGER.error(f"Neo HTTP error: {e}")
            return None
