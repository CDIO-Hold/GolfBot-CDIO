from Vector import Vector
from DistanceMath import DistanceMath


class Line:
    def __init__(self, start: Vector, end: Vector):
        self.start = start
        self.end = end
        self.length = DistanceMath.real_distance(start, end)

    def distance_to(self, point: Vector):
        part1 = (self.end.y - self.start.y) * point.x
        part2 = (self.end.x - self.start.x) * point.y
        part3 = self.end.x * self.start.y - self.end.y * self.start.x

        numerator = abs(part1 - part2 + part3)
        denominator = self.length
        return numerator / denominator


class Shape:
    def intersects(self, line: Line):
        raise NotImplementedError()

    def get_center(self):
        raise NotImplementedError()


class Box(Shape):
    def __init__(self, top_left: Vector, bottom_right: Vector):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def intersects(self, line: Line):
        own_lines = [Line(self.top_left, Vector(self.bottom_right.x, self.top_left.y)),
                     Line(Vector(self.bottom_right.x, self.top_left.y), self.bottom_right),
                     Line(self.bottom_right, Vector(self.top_left.x, self.bottom_right.y)),
                     Line(Vector(self.top_left.x, self.bottom_right.y), self.top_left)]

        # Literally stolen from https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
        def ccw(A, B, C):
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

        intersection = False
        for own_line in own_lines:
            a, b = line.start, line.end
            c, d = own_line.start, own_line.end

            if intersect(a, b, c, d):
                intersection = True
                break
        return intersection

    def get_center(self):
        return Vector((self.top_left.x + self.bottom_right.x) / 2, (self.top_left.y + self.bottom_right.y) / 2)


class Circle(Shape):
    def __init__(self, center: Vector, diameter: int):
        self.center = center
        self.diameter = diameter

    def intersects(self, line: Line):
        return line.distance_to(self.center) < (self.diameter / 2)

    def get_center(self):
        return self.center


class Ball(Circle):
    def __init__(self, center: Vector, color: str, diameter: int):
        super().__init__(center, diameter=diameter)
        self.color = color


class Field:
    def __init__(self):
        self.width = 1800
        self.height = 1200
        self.balls = []
        self.obstacles = []

    @property
    def corners(self):
        return [
            Vector(0, 0),
            Vector(self.width, 0),
            Vector(self.width, self.height),
            Vector(0, self.height)
        ]

    @property
    def safe_zones(self):
        quarter_width = self.width // 4
        quarter_height = self.height // 4
        return [
            Vector(quarter_width, quarter_height * 2),
            Vector(quarter_width * 2, quarter_height),
            Vector(quarter_width * 3, quarter_height * 2),
            Vector(quarter_width * 2, quarter_height * 3)
        ]

    def insert_cross(self, center: Vector):
        left_x = center.x - 100
        right_x = center.x + 100
        top_y = center.y + 100
        bottom_y = center.y - 100

        cross_width = 30
        half_width = int(cross_width // 2)

        horizontal = Box(Vector(left_x, center.y - half_width), Vector(right_x, center.y + half_width))
        vertical = Box(Vector(center.x - half_width, top_y), Vector(center.x + half_width, bottom_y))
        self.obstacles.append(horizontal)
        self.obstacles.append(vertical)

    def insert_egg(self, center: Vector):
        egg_width = 100
        egg = Circle(center, diameter=egg_width)
        self.obstacles.append(egg)

    def insert_ball(self, center: Vector, color: str):
        ball_width = 40
        ball = Ball(center, color, diameter=ball_width)
        self.balls.append(ball)

    def can_drive_straight(self, start: Vector, end: Vector):
        drive_line = Line(start, end)
        return self.can_drive_line(drive_line)

    def can_drive_line(self, drive_line: Line):
        for obstacle in self.obstacles:
            if obstacle.intersects(drive_line):
                return False
        return True

    def get_seen_balls(self, position: Vector):
        return [ball for ball in self.balls if self.can_drive_straight(position, ball.get_center())]


def nearest_of(position: Vector, candidates: list):
    nearest = None
    min_distance = float('inf')
    for other in candidates:
        distance = DistanceMath.real_distance(position, other.center)
        if distance < min_distance:
            min_distance = distance
            nearest = other
    return nearest
