from socket import socket, AF_INET, SOCK_DGRAM
from Vector import Vector


class Server:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def connect(self, ip_address: str, port: int):
        self.socket.connect((ip_address, port))

    def send(self, message: str) -> str:
        self.socket.send(message.encode("utf-8"))
        return self.socket.recv(1024).decode("utf-8")

    def update_robot(self, position: Vector, degrees: float):
        self.send(f"robot {position.x},{position.y} {degrees}")

    def move_robot(self, target: Vector):
        self.send(f"goto {target.x},{target.y}")

    def collect(self):
        self.send("collect")

    def unload(self):
        self.send("shoot")

    def stop_conveyors(self):
        self.send("stop")

    def close(self):
        self.send("exit")
        self.socket.close()
