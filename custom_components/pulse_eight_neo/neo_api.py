import logging
import http.client

_LOGGER = logging.getLogger(__name__)

class NeoMatrix:
    def __init__(self, host):
        self.host = host

    def route(self, output, input):
        # Convert to zero-based
        out = int(output) - 1
        inp = int(input) - 1

        path = f"/Port/Set/{out}/{inp}"
        _LOGGER.warning(f"Neo HTTP -> http://{self.host}{path}")

        try:
            conn = http.client.HTTPConnection(self.host, timeout=3)
            conn.request("GET", path)
            response = conn.getresponse()
            response.read()
            conn.close()
            return response.status
        except Exception as e:
            _LOGGER.error(f"Neo HTTP error: {e}")
            return None
