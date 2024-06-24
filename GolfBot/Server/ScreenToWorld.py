from Vector import Vector
from Shapes import Box
from Camera import Camera
from Angle import Angle
from Shapes import Shape


class ScreenToWorld:
    def __init__(self, camera: Camera):
        self.height = camera.image_height

    def convert_vector(self, vector: Vector) -> Vector:
        return Vector(vector.x, self.height - vector.y)

    def convert_box(self, box: Box) -> Box:
        top_left = self.convert_vector(box.top_left)
        bottom_right = self.convert_vector(box.bottom_right)
        return Box(top_left, bottom_right)

    def convert_angle(self, angle: Angle) -> Angle:
        return angle * -1
