from Position import Position
from Circle import Circle
from Angle import Angle, degrees
from RobotMathematics import AngleMath, DistanceMath
from DriveSpeed import DriveSpeed
from Vector import Vector


class Driver:
    def __init__(self,
                 move_tank,
                 speed: DriveSpeed,
                 wheel: Circle,
                 turn_circle: Circle):
        self.tank = move_tank
        self.speed = speed
        self.wheel = wheel
        self.turn_circle = turn_circle

    def turn(self, angle: Angle):
        turn_degrees = angle.get_value(signed=True, unit=degrees)
        print("Turning:", turn_degrees, "degrees")

        if turn_degrees < 0:
            self.tank.turn_left(self.speed.rotate_speed, abs(turn_degrees))
        else:
            self.tank.turn_right(self.speed.rotate_speed, turn_degrees)

    def drive(self, distance: float):
        rotations = distance / self.wheel.circumference

        self.tank.on_for_rotations(
            self.speed.straight_speed,
            self.speed.straight_speed,
            rotations
        )

    def stop(self):
        self.tank.off()
