#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Create the ev3
ev3 = EV3Brick()

# Initialize the motors
left_wheel = Motor(Port.D)
right_wheel = Motor(Port.A)


# Initialize the robot
Robot = DriveBase(left_wheel, right_wheel, wheel_diameter=65, axle_track=104)
current_settings = robot.settings()
new_settings = (500, current_settings[1], current_settings[2], current_settings[3])
Robot.settings(new_settings[0], new_settings[1], new_settings[2], new_settings[3])


# This function gets two coordinates and drives the robot to the destination
def drive_to_dest(x, y):
    # for now the robots coordinates
    current_robot_x, current_robot_y = 0, 0

    # The distance Robot needs to drive to reach destination 
    distance_x = x - current_robot_x
    distance_y = y - current_robot_y

    # Calculate the angle to turn to
    angle_to_turn = 50  #depends on where the (ball) is located

    robot.turn(angle_to_turn)

    # Drive straight to reach the coordinates
    while Robot.distance() < distance_x:
        Robot.straight(distance_x)
        Robot.stop()
        left_wheel.brake()
        right_wheel.brake()

        Robot.turn(angle_to_turn)

        Robot.straight(distance_y)
        Robot.stop()
        left_wheel.brake()
        right_wheel.brake()
    
    
# 1 meter in x axis
destination_x = 1000
destination_y = 0

drive_to_dest(destination_x, destination_y)
