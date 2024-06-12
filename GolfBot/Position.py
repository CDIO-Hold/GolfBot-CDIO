class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) is Position:
            return Position(self.x + other.x, self.y + other.y)
        raise ValueError("Cannot add a position to a non-position")
