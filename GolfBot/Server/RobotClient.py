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
    def __init__(self, screen_to_world: ScreenToWorld):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.converter = screen_to_world

    def connect(self, ip_address: str, port: int):
        self.socket.connect((ip_address, port))

    def send(self, message: str, expect_answer: bool = True) -> str:
        self.socket.send(message.encode("utf-8"))
        if not expect_answer:
            return None
        return self.socket.recv(1024).decode("utf-8")

    def update_info(self, screen_position: Vector, screen_angle: float):
        robot_position = self.converter.convert_vector(screen_position)
        robot_angle = self.converter.convert_angle(screen_angle)

        self.send(f"robot {robot_position.x},{robot_position.y} {robot_angle}")

    def move_to(self, screen_position: Vector):
        robot_position = self.converter.convert_vector(screen_position)

        self.send(f"goto {robot_position.x},{robot_position.y}")

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
