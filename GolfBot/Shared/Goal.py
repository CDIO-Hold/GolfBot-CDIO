from .Position import Position


class Goal:
    def __init__(self, name, position: Position, score):
        self.name = name
        self.position = position
        self.score = score
