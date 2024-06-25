from socket import socket, AF_INET, SOCK_DGRAM
from Vector import Vector
from Camera import Camera
from Shapes import Box
from Angle import Angle

class ScreenToWorld:
    def __init__(self, camera: Camera, scale: float = 1.0):
        self.height = camera.image_height
        self.scale = scale

    def convert_vector(self, vector: Vector) -> Vector:
        return Vector(vector.x, self.height - vector.y) * self.scale

    def convert_box(self, box: Box) -> Box:
        top_left = self.convert_vector(box.top_left)
        bottom_right = self.convert_vector(box.bottom_right)
        return Box(top_left, bottom_right)

    def convert_angle(self, angle: Angle) -> Angle:
        return angle * -1


class RobotClient:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def connect(self, ip_address: str, port: int):
        self.socket.connect((ip_address, port))

    def send(self, message: str, expect_answer: bool = True) -> str:
        self.socket.send(message.encode("utf-8"))
        if not expect_answer:
            return None
        return self.socket.recv(1024).decode("utf-8")

    def update_info(self, position: Vector, angle: float):
        self.send(f"robot {position.x},{position.y} {angle}")

    def move_to(self, position: Vector):
        self.send(f"goto {position.x},{position.y}")

    def collect(self):
        self.send("collect")

    def unload(self):
        self.send("shoot")

    def stop_conveyors(self):
        self.send("stop")

    def get_info(self):
        return self.send("info", expect_answer=True)

    def close(self):
        self.send("exit", expect_answer=False)
        self.socket.close()
