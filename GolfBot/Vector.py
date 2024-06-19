import math
from Position import Position
from Angle import Angle
from RobotMathematics import AngleMath


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_points(cls, start: Position, end: Position):
        delta_x = end.x - start.x
        delta_y = end.y - start.y
        return cls(delta_x, delta_y)

    @property
    def square_length(self) -> float:
        return self.x * self.x + self.y * self.y

    @property
    def length(self) -> float:
        return math.sqrt(self.square_length)

    @property
    def angle(self) -> Angle:
        # Simplified from the general formula of angle between vectors
        return AngleMath.atan2(self.y, self.x)

    def __str__(self):
        return "(" + str(self.x) + "; " + str(self.y) + ")"

    def __eq__(self, other):
        if type(other) is Vector:
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        return not (self == other)

    @staticmethod
    def angle_between(v, w) -> Angle:
        return AngleMath.atan2(v.y * w.x - v.x * w.y, v.x * w.x + v.y * w.y)
