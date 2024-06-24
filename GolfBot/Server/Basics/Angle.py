import math


class AngleUnit:
    def __init__(self, maximum_exclusive: float, string_representation: str):
        self.maximum = maximum_exclusive
        self.representation = string_representation

    def conversion_factor(self, other):
        if type(other) is AngleUnit:
            return other.maximum / self.maximum
        else:
            return None

    def __str__(self):
        return self.representation


degrees = AngleUnit(360.0, "degrees")
radians = AngleUnit(2 * math.pi, "radians")
percent = AngleUnit(100, "percent")


class Angle:
    def __init__(self, value: float, unit: AngleUnit):
        self.value = value % unit.maximum
        self.unit = unit

    def with_unit(self, new_unit: AngleUnit):
        new_value = self.value * self.unit.conversion_factor(new_unit)
        return Angle(new_value, new_unit)

    def opposite(self):
        return Angle(self.unit.maximum - self.value, self.unit)

    def get_value(self, signed=True, unit=None):
        # If no unit is given, use the unit of this Angle
        unit = self.unit if unit is None else unit

        factor = self.unit.conversion_factor(unit)
        value = self.value * factor

        if signed:
            cutoff = unit.maximum / 2
            if value > cutoff:
                value = value - unit.maximum

        return value

    @property
    def signed_value(self):
        return self.get_value()

    def __str__(self):
        return str(self.signed_value) + " " + str(self.unit)

    def __add__(self, other):
        if type(other) is Angle:
            return Angle(self.value + other.get_value(unit=self.unit), self.unit)
        elif type(other) is int or type(other) is float:
            return Angle(self.value + other, self.unit)
        raise ValueError("Cannot add non-angle to an angle")

    def __sub__(self, other):
        return self + (other * -1)

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Angle(self.value * other, self.unit)
        raise ValueError("Cannot multiply an angle by a non-number")

    def __eq__(self, other):
        if type(other) is Angle:
            return self.value == other.get_value(unit=self.unit)
        return False

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        if type(other) is Angle:
            return self.value > other.get_value(unit=self.unit)
        return False

    def __ge__(self, other):
        return (self > other) or (self == other)

    def __lt__(self, other):
        if type(other) is Angle:
            return self.value < other.get_value(unit=self.unit)
        return False

    def __le__(self, other):
        return (self < other) or (self == other)

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)


class CardinalDirection:
    @staticmethod
    @property
    def EAST():
        return Angle(0, degrees)

    @staticmethod
    @property
    def NORTH():
        return Angle(90, degrees)

    @staticmethod
    @property
    def WEST():
        return Angle(180, degrees)

    @staticmethod
    @property
    def SOUTH():
        return Angle(270, degrees)

    @staticmethod
    def angle_to_cardinal(angle: Angle):
        angle = angle.get_value(signed=True, unit=degrees)
        if 45 <= angle < 135:
            return CardinalDirection.NORTH
        elif -45 <= angle < 45:
            return CardinalDirection.EAST
        elif angle >= 135 or angle < -135:
            return CardinalDirection.WEST
        else:
            return CardinalDirection.SOUTH


class AngleMath:
    @staticmethod
    def acos(x) -> Angle:
        print("Acos of " + str(x))
        return Angle(math.acos(x), radians)

    @staticmethod
    def asin(x) -> Angle:
        return Angle(math.asin(x), radians)

    @staticmethod
    def atan(x) -> Angle:
        return Angle(math.atan(x), radians)

    @staticmethod
    def atan2(y, x) -> Angle:
        return Angle(math.atan2(y, x), radians)

    @staticmethod
    def get_radians(angle) -> float:
        if type(angle) is int or type(angle) is float:
            return angle
        else:
            return angle.get_value(signed=False, unit=radians)

    @staticmethod
    def cos(x) -> float:
        return math.cos(AngleMath.get_radians(x))

    @staticmethod
    def sin(x) -> float:
        return math.sin(AngleMath.get_radians(x))

    @staticmethod
    def tan(x) -> float:
        return math.tan(AngleMath.get_radians(x))
