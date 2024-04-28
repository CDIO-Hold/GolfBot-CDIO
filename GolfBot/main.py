#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import atan2, degrees, sqrt

# Create the ev3
ev3 = EV3Brick()

# Initialize the motors
left_wheel = Motor(Port.D)
right_wheel = Motor(Port.A)
right_motor_for_balls = Motor(Port.C)
left_motor_for_balls = Motor(Port.B)


# Initialize the robot
Robot = DriveBase(left_wheel, right_wheel, wheel_diameter=65, axle_track=104)
current_settings = Robot.settings()
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

    Robot.turn(angle_to_turn)

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

# Drive to goal-destination
def Drive_to_goal(x, y):
    current_robot_x, current_robot_y = 0, 0

    # The distance Robot needs to drive to reach destination
    distance_x = x - current_robot_x
    distance_y = y - current_robot_y

    # Drive the robot to goal
    Drive_to_goal(50, 500)

    #Rotate the motor for the balls, for the balls to get into the goal
    left_wheel.brake()
    right_wheel.brake()
    left_motor_for_balls.run(5) #Test, and see that the speed should be
    right_motor_for_balls.run(5) #Test, and see that the speed should be
