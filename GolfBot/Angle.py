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

    @property
    def signed_value(self):
        cutoff = self.unit.maximum / 2
        if self.value > cutoff:
            return self.value - self.unit.maximum
        else:
            return self.value

    def __str__(self):
        return str(self.value) + " " + str(self.unit)

    def __add__(self, other):
        if type(other) is Angle:
            if self.unit == other.unit:
                factor = 1
            else:
                factor = other.unit.conversion_factor(self.unit)
            return Angle(self.value + other.value * factor, self.unit)
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
            if self.unit == other.unit:
                return self.value == other.value
            factor = other.unit.conversion_factor(self.unit)

            return self.value == (other.value * factor)
        return False

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        if type(other) is Angle:
            if self.unit == other.unit:
                return self.value > other.value
            factor = other.unit.conversion_factor(self.unit)

            return self.value > (other.value * factor)
        return False

    def __ge__(self, other):
        return (self > other) or (self == other)

    def __lt__(self, other):
        if type(other) is Angle:
            if self.unit == other.unit:
                return self.value < other.value
            factor = other.unit.conversion_factor(self.unit)

            return self.value < (other.value * factor)
        return False

    def __le__(self, other):
        return (self < other) or (self == other)

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)
