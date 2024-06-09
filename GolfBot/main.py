#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from GolfBot.Driver import Driver
from GolfBot.Position import Position

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
