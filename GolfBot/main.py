'''
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from GolfBot.Shared import Position

#from GolfBot.Position import Position


# Create the ev3
ev3 = EV3Brick()

# Initialize the motors
right_wheel = Motor(Port.B)
left_wheel = Motor(Port.C)

# Initialize the driver
driver = Driver(left_wheel, right_wheel)

#left_wheel.run_time(1000, 5000)
right_wheel.run_time(800, 100)



path = [Position(1000, 0), Position(500, 300), Position(-200, 200), Position(0, 0)]
# 1 meter in x axis
destination_x = 1000
destination_y = 0

path = [Position(1000, 0), Position(500, 300), Position(-200, 200), Position(0, 0)]
for point in path:
    driver.drive_to(point)
    print("Position:", driver.position)
    print("Direction:", driver.rotation)
'''
from GolfBot.Robot import Driver

if __name__ == "__main__":
    import rpyc
    print("RPyC imported")
    #from Robot.Driver import Driver

    # conn = rpyc.classic.connect("192.168.124.17")
    print("Connecting to EV3...")
    conn = rpyc.classic.connect("172.20.10.12", port=18812)
    print("Connected to EV3")

    ev3dev_motor = conn.modules['ev3dev2.motor']

    right_wheel = ev3dev_motor.LargeMotor(ev3dev_motor.OUTPUT_B)
    left_wheel = ev3dev_motor.LargeMotor(ev3dev_motor.OUTPUT_C)
    right_conveyor = ev3dev_motor.MediumMotor(ev3dev_motor.OUTPUT_A)
    left_conveyor = ev3dev_motor.MediumMotor(ev3dev_motor.OUTPUT_D)

    #driver = Driver(left_wheel, right_wheel)

    #https://github.com/Stonebank/CDIO-3/blob/main/src/remoteControl.py
    # bruger tank istead for Driver
    #tank = ev3dev_motor.MoveTank(ev3dev_motor.OUTPUT_A, ev3dev_motor.OUTPUT_B)

    while True:
        command = input()
        if command == "exit":
            break

        if command == "w":
            left_wheel.run_forever(speed_sp=200)
            right_wheel.run_forever(speed_sp=200)
            #tank.on(200,200)
        if command == "b":
            left_wheel.run_forever(speed_sp=-200)
            right_wheel.run_forever(speed_sp=-200)
        elif command == "x":
            left_wheel.run_forever(speed_sp=-150)
            right_wheel.run_forever(speed_sp=-150)
        elif command == "d":
            left_wheel.run_forever(speed_sp=100)
            right_wheel.run_forever(speed_sp=-100)
        elif command == "a":
            left_wheel.run_forever(speed_sp=-100)
            right_wheel.run_forever(speed_sp=100)
        elif command == "s":
            left_wheel.stop()
            right_wheel.stop()
        elif command == "r":
            right_conveyor.run_forever(speed_sp=500)
            left_conveyor.run_forever(speed_sp=-500)
        elif command == "t":
            right_conveyor.run_forever(speed_sp=-500)
            left_conveyor.run_forever(speed_sp=500)
        elif command == "f":
            right_conveyor.stop()
            left_conveyor.stop()
        elif command =="p":
            Driver.drive_to(100,100)





    ev3dev2_motor = conn.modules['ev3dev2.motor']
    #motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_C)

    print("Disconnected from the EV3")