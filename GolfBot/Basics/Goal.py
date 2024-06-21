from .Vector import Vector


class Goal:
    def __init__(self, name, position: Vector, score: int):
        self.name = name
        self.position = position
        self.score = score
