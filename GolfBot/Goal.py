from Basics import Vector


class Goal:
    def __init__(self, name, position: Vector, score):
        self.name = name
        self.position = position
        self.score = score
