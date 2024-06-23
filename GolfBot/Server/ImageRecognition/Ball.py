from GolfBot.Server.Basics import Vector
from GolfBot.Server.ImageRecognition import DetectedObject


class Ball(DetectedObject):
    def __init__(self, name: str, position: Vector, diameter: float):
        self.position = position
        self.diameter = diameter
