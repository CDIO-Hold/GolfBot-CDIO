import math
from GolfBot.Basics import Angle, AngleMath


# (Private) Helper method for some parts of construction
def _is_number(x):
    return type(x) is int or type(x) is float


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

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

    def lengthen(self, amount: float):
        self.x *= amount
        self.y *= amount

    def shorten(self, amount: float):
        self.lengthen(1 / amount)

    def __eq__(self, other):
        if type(other) is Vector:
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        return not (self == other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, other):
        if type(other) is Vector:
            return Vector(self.x + other.x, self.y + other.y)
        raise ValueError("Cannot add a position to a non-position")

    def __sub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Vector(self.x * other, self.y * other)
        raise ValueError("Cannot multiply a vector with a non-number")

    def __getitem__(self, item: int) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        raise IndexError("Vector only contains x and y (not '" + str(key) + "')")

    def __setitem__(self, key: int, value: int):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        raise IndexError("Vector only contains x and y (not '" + str(key) + "')")

    def __copy__(self):
        return Vector(self.x, self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def normalized(self):
        normal = self.__copy__()
        normal.shorten(self.length)
        return normal

    # Alternate constructors
    @classmethod
    def from_points(cls, start, end):
        delta_x = end.x - start.x
        delta_y = end.y - start.y
        return cls(delta_x, delta_y)

    @classmethod
    def from_magnitude_and_direction(cls, magnitude: float, direction: Angle):
        x = magnitude * AngleMath.cos(direction)
        y = magnitude * AngleMath.sin(direction)
        return cls(x, y)

    # Conversions
    def as_tuple(self) -> (float, float):
        return self.x, self.y

    @classmethod
    def from_tuple(cls, value: (float, float)):
        return cls(value[0], value[1])

    def as_list(self) -> list:
        return [self.x, self.y]

    @classmethod
    def from_list(cls, value: list):
        if len(list) != 2:
            raise ValueError("Cannot convert list with anything other than 2 values to a vector")
        if not (_is_number(value[0]) and _is_number(value[1])):
            raise ValueError("Cannot convert list with non-numbers to a vector")
        return cls(value[0], value[1])

    # Operations
    @staticmethod
    def angle_of(v) -> Angle:
        return Vector.angle_between(v, Vector(0, 0))

    @staticmethod
    def angle_between(v, w) -> Angle:
        return AngleMath.atan2(v.y * w.x - v.x * w.y, v.x * w.x + v.y * w.y)
