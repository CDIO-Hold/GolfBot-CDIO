from Vector import Vector
from DistanceMath import DistanceMath
from Shapes import Box as ScreenBox


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

        intersecting = False
        for own_line in own_lines:
            a, b = line.start, line.end
            c, d = own_line.start, own_line.end

            if intersect(a, b, c, d):
                intersecting = True
                break
        return intersecting

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

    def is_inside(self, position: Vector):
        return 0 <= position.x <= self.width and 0 <= position.y <= self.height

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


class ScreenToWorld:
    def __init__(self):
        self.height_scale = 1
        self.width_scale = 1

        self.x_offset = 0
        self.y_offset = 0

    def calibrate_from_walls(self, screen_wall_boxes: list[ScreenBox]):
        left_right = sorted(screen_wall_boxes, key=lambda box: box.width)[:2]
        top_bottom = sorted(screen_wall_boxes, key=lambda box: box.height)[:2]

        left, right = sorted(left_right, key=lambda box: box.get_center().x)
        top, bottom = sorted(top_bottom, key=lambda box: box.get_center().y)

        box = ScreenBox(Vector(left.x1, top.y1), Vector(right.x2, bottom.y2))
        self.calibrate(box)

    def calibrate(self, screen_field: ScreenBox):
        self.height_scale = 1200 / screen_field.height
        self.width_scale = 1800 / screen_field.width

        self.x_offset = screen_field.top_left.x
        self.y_offset = screen_field.top_left.y

    def vector(self, position: Vector) -> Vector:
        return Vector(
            (position.x - self.x_offset) * self.width_scale,
            1200 - (position.y - self.y_offset) * self.height_scale
        )


if __name__ == '__main__':
    walls = [
            ScreenBox(Vector(191, 3), Vector(226, 680)),
            ScreenBox(Vector(1022, 9), Vector(1058, 669)),
            ScreenBox(Vector(187, 17), Vector(1059, 35)),
            ScreenBox(Vector(168, 633), Vector(1084, 658)),
        ]

    screen_to_world = ScreenToWorld()
    screen_to_world.calibrate_from_walls(walls)
    print(screen_to_world.vector(Vector(191, 3)))
