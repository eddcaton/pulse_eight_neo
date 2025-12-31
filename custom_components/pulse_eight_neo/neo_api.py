import socket
import logging

_LOGGER = logging.getLogger(__name__)

class NeoMatrix:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def send(self, cmd):
        _LOGGER.warning(f"Neo sending to {self.host}:{self.port} -> {cmd.strip()}")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((self.host, self.port))
                s.sendall(cmd.encode("ascii"))
                try:
                    return s.recv(1024).decode("ascii")
                except:
                    return None
        except Exception as e:
            _LOGGER.error(f"Neo socket error: {e}")
            return None

    def route(self, output, input):
        # Official Pulse-Eight Neo format
        cmd = f"SET OUT{output} IN{input}\r\n"
        return self.send(cmd)

    def power_on(self, output):
        return self.send(f"CEC ON OUT{output}\r\n")

    def power_off(self, output):
        return self.send(f"CEC OFF OUT{output}\r\n")
