import math
from GolfBot.Shared import Position
from GolfBot.Robot import Speed
from GolfBot.Robot import Circle
from GolfBot.Shared import Angle, degrees


class Driver:
    def __init__(self,
                 move_tank,
                 speed: Speed,
                 wheel: Circle,
                 turn_circle: Circle,
                 starting_rotation = 0.0,
                 starting_position = (0, 0)):
        self.tank = move_tank
        self.speed = speed
        self.wheel = wheel
        self.turn_circle = turn_circle

        if type(starting_rotation) is float:
            self.rotation = Angle(starting_rotation, degrees)
        else:
            self.rotation = starting_rotation

        if type(starting_position) is tuple:
            self.position = Position(starting_position[0], starting_position[1])
        else:
            self.position = starting_position

    def set_rotation(self, angle):
        self.rotation = angle % 360

    def set_coordinates(self, x: float, y: float):
        self.position = Position(x, y)

    def turn(self, degrees):
        # Make the degree in the interval 0 - 360
        degrees %= 360

        self.rotation = (self.rotation + degrees) % 360

    def turn_to(self, target_angle):
        target_angle = (target_angle % 360)

        self.tank.turn_degrees(self.speed.rotate_speed, target_angle)

    def drive(self, distance):
        rotations = distance / self.wheel.circumference

        self.tank.on_for_rotations(
            self.speed.straight_speed,
            self.speed.straight_speed,
            rotations
        )

        self.position.x += math.cos(self.rotation) * distance
        self.position.y += math.sin(self.rotation) * distance

    def drive_to(self, target_position: Position):
        delta_x = target_position.x - self.position.x
        delta_y = target_position.y - self.position.y

        drive_angle = math.acos(delta_x)
        self.turn_to(drive_angle)

        distance = math.sqrt(delta_x*delta_x + delta_y*delta_y)
        self.drive(distance)

    def follow_path(self, path: list):
        for position in path:
            target_position = Position(position[0], position[1])
            self.drive_to(target_position)