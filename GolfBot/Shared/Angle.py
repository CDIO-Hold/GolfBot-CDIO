import math

class AngleUnit:
    def __init__(self, minimum: float, maximum: float, representation: str):
        self.minimum = minimum
        self.maximum = maximum
        self.representation = representation

    def __str__(self):
        return self.representation

    def __repr__(self):
        return self.representation


degrees = AngleUnit(0, 360, "degrees")
radians = AngleUnit(0, 2 * math.pi, "radians")

class Angle:
    def __init__(self, value: float, unit: AngleUnit = degrees):
        self.value = value
        self.unit = unit

    def convert_unit(self, new_unit: AngleUnit):
        unit_value = ((self.value - self.unit.minimum) / self.unit.maximum)
        scaled_value = ((unit_value * new_unit.maximum) + new_unit.minimum)

        self.value = scaled_value
        self.unit = new_unit

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __repr__(self):
        return f"{self.value} {self.unit}"

if __name__ == '__main__':
    v = Angle(180, degrees)
    print(v.value)
    v.convert_unit(radians)
    print(v.value)
    v.convert_unit(degrees)
    print(v.value)
