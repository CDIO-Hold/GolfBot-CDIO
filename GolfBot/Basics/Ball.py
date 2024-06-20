from GolfBot.Basics import Vector


class Ball:
    def __init__(self, name: str, position: Vector, size: int = 1):
        self.name = name
        self.position = position
        self.size = size
