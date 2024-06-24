import math
from GolfBot.Server.Basics import Vector, Angle


class Shape:
    def get_center(self) -> Vector:
        return NotImplemented("Shape is abstract")


class Box(Shape):
    def __init__(self, top_left: Vector, bottom_right: Vector):
        self.top_left = top_left
        self.bottom_right = bottom_right

    @property
    def x1(self) -> float:
        return self.top_left.x

    @property
    def y1(self) -> float:
        return self.top_left.y

    @property
    def x2(self) -> float:
        return self.bottom_right.x

    @property
    def y2(self) -> float:
        return self.bottom_right.y

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def dimensions(self) -> (float, float):
        return self.width, self.height

    def get_center(self):
        return Vector((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)


class Circle(Shape):
    def __init__(self, center: Vector, **kwargs):
        self.center = center

        if "radius" in kwargs:
            self.radius = kwargs["radius"]
        elif "diameter" in kwargs:
            self.radius = kwargs["diameter"] / 2.0
        else:
            raise ValueError("Either radius or diameter has to have a value")

    @property
    def diameter(self) -> float:
        return self.radius * 2

    @property
    def circumference(self) -> float:
        return self.diameter * math.pi

    @property
    def area(self) -> float:
        return self.radius * self.radius * math.pi

    @property
    def get_center(self) -> Vector:
        return self.center


class MultiShape(Shape):
    def __init__(self, *shapes: Shape):
        self.shapes = list(shapes)

    def get_center(self) -> Vector:
        center_sum = Vector(0, 0)
        for shape in self.shapes:
            center_sum += shape.get_center()

        return center_sum * (1 / len(self.shapes))


class AngledShape:
    def __init__(self, shape: Shape, angle: Angle):
        self.shape = shape
        self.angle = angle
