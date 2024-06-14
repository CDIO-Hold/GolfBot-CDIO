import rpyc
from Driver import Driver
from Speed import Speed
from Circle import Circle

conn = rpyc.classic.connect("192.168.196.17", 18812)

ev3dev2_motor = conn.modules['ev3dev2.motor']
ev3dev2_conveyor_motor = conn.modules['ev3dev2.motor']
ev3dev2_sensor = conn.modules['ev3dev2.sensor.lego']

left_port = ev3dev2_motor.OUTPUT_C
right_port = ev3dev2_motor.OUTPUT_B
right_conveyor = ev3dev2_motor.OUTPUT_A
left_conveyor = ev3dev2_motor.OUTPUT_D

right = ev3dev2_motor.LargeMotor(right_port)
left = ev3dev2_motor.LargeMotor(left_port)
right_con = ev3dev2_motor.MediumMotor(right_conveyor)
left_con = ev3dev2_motor.MediumMotor(left_conveyor)

tank = ev3dev2_motor.MoveTank(left_port, right_port)
conveyor_tank = ev3dev2_motor.MoveTank(right_conveyor, left_conveyor)
tank.gyro = ev3dev2_sensor.GyroSensor()

speed = Speed(40,10)
wheel = Circle(diameter=68.8)
driver = Driver(tank,conveyor_tank, speed, wheel, Circle(0))
#driver.drive(1000)
#driver.turn_to(90)
driver.run_conveyor()

#tank.on_for_rotations(speed, speed, rotations)
#tank.on_for_rotations(speed, speed, rotations)
#tank.on_for_rotations(speed, speed, -rotations)

exit(0)

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import atan2, degrees, sqrt
import time





