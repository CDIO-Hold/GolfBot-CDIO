from GolfBot.Server.Basics import Box
from ImageRecognition import DetectedObject


class HalfCross(DetectedObject):
    def __init__(self):
        pass


class Cross:
    def __init__(self, name, position: Box):
        self.name = name
        self.position = position
