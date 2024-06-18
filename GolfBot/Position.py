class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) is Position:
            return Position(self.x + other.x, self.y + other.y)
        raise ValueError("Cannot add a position to a non-position")

    def __str__(self):
        return "(" + str(self.x) + "; " + str(self.y) + ")"

    def __getitem__(self, item: int) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        raise IndexError("Position only contains the indices 0 and 1 (not '" + str(item) + "')")

    def __setitem__(self, key: int, value: int):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        raise IndexError("Position only contains the indices 0 and 1 (not '" + str(key) + "')")

    def __copy__(self):
        return Position(self.x, self.y)

    def as_tuple(self) -> (float, float):
        return self.x, self.y

    @classmethod
    def from_tuple(cls, value: (float, float)):
        return cls(value[0], value[1])
