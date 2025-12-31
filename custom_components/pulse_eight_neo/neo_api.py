import socket

class NeoMatrix:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((self.host, self.port))
            s.sendall(cmd.encode("ascii"))
            try:
                return s.recv(1024).decode()
            except:
                return None

    def route(self, output, input):
        # This is the Pulse-Eight routing format
        # Format used by Neo series:
        # SET OUTx INy
        cmd = f"SET OUT{output} IN{input}\r\n"
        return self.send(cmd)

    def power_on(self, output):
        return self.send(f"CEC ON OUT{output}\r\n")

    def power_off(self, output):
        return self.send(f"CEC OFF OUT{output}\r\n")
