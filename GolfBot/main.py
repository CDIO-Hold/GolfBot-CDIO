#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import math


def value_or_default(value, default):
    return default if value is None else default


def degrees_to_radians(degrees: float):
    return (degrees / 180) * math.pi


def radians_to_degrees(radians: float):
    return (radians / math.pi) * 180


class Position:
    def __init__(self, x, y, angle=None):
        self.x = x
        self.y = y
        self.angle = angle

    @property
    def has_angle(self):
        return self.angle is not None

    def __str__(self):
        return "(" + str(self.x) +"; " + str(self.y) + ")"


class Driver:
    wheel_diameter = 6.88
    wheel_distance = 13.5

    def __init__(self, left_motor, right_motor, drive_speed: float = 1000, rotate_speed: float = None):
        self.drive_speed = drive_speed
        self.rotate_speed = value_or_default(rotate_speed, drive_speed)

        self.base = DriveBase(left_motor, right_motor, self.wheel_diameter * 10, self.wheel_distance * 10)
        #self.base.settings(straight_speed=drive_speed)
        self.rotation = 0.0
        self.position = Position(0.0, 0.0)

        self.wheel_circumference = self.wheel_diameter * math.pi
        self.rotation_circumference = self.wheel_distance * math.pi

    def set_rotation(self, angle):
        self.rotation = angle % 360

    def set_coordinates(self, x, y):
        self.position = Position(x, y)

    def turn(self, degrees):
        """
        if degrees > 180:
            degrees = -(degrees - 180)
        elif degrees < -180:
            degrees = -(degrees + 180)
        """

        self.base.turn(-degrees)
        self.rotation = (self.rotation + degrees) % 360

    def turn_to(self, target_angle):
        delta_angle = (target_angle - self.rotation)
        self.turn(delta_angle)

    def drive(self, distance):
        self.base.straight(distance)
        self.base.stop()

        heading_radians = degrees_to_radians(self.rotation)
        self.position.x += math.cos(heading_radians) * distance
        self.position.y += math.sin(heading_radians) * distance

    def drive_to(self, target_position: Position):
        delta_x = target_position.x - self.position.x
        delta_y = target_position.y - self.position.y
        distance = math.sqrt(delta_x*delta_x + delta_y*delta_y)

        drive_angle = radians_to_degrees(math.atan2(delta_y, delta_x))
        print("Distance:", distance)
        print("Drive angle:", drive_angle)
        self.turn_to(drive_angle)

        self.drive(distance)

        if target_position.has_angle:
            self.turn_to(target_position.angle)

# Create the ev3
ev3 = EV3Brick()

# Initialize the motors
right_wheel = Motor(Port.B)
left_wheel = Motor(Port.C)

# Initialize the driver
driver = Driver(left_wheel, right_wheel)

path = [Position(1000, 0), Position(500, 300), Position(-200, 200), Position(0, 0)]
# 1 meter in x axis
destination_x = 1000
destination_y = 0

for point in path:
    driver.drive_to(point)
    print("Position:", driver.position)
    print("Direction:", driver.rotation)

if __name__ == "__main__":
    import rpyc

    conn = rpyc.classic.connect("192.168.124.17")

    ev3dev2_motor = conn.modules['ev3dev2.motor']

    motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_C)

    #motor = conn.modules['ev3dev2.motor'].MediumMotor(conn.modules['ev3dev2.motor'].OUTPUT_D)

    motor.run_forever(speed_sp=1000)
