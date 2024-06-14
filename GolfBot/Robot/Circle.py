import math


class Circle:
    def __init__(self, radius: float = None, diameter: float = None):
        if radius is not None:
            self.radius = radius
        elif diameter is not None:
            self.radius = diameter / 2.0
        else:
            raise ValueError("Either radius or diameter has to have a value")

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def circumference(self):
        return self.diameter * math.pi

    @property
    def area(self):
        return self.radius * self.radius * math.pi