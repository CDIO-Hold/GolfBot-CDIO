import rpyc
from .Robot import Driver
from .Robot import Speed
from .Robot import Circle


print("Connecting to EV3...")
conn = rpyc.classic.connect("192.168.196.17", 18812)
print("Connected to EV3")

ev3dev2_motor = conn.modules['ev3dev2.motor']
ev3dev2_sensor = conn.modules['ev3dev2.sensor.lego']

left_port = ev3dev2_motor.OUTPUT_C
right_port = ev3dev2_motor.OUTPUT_B
right_conveyor = ev3dev2_motor.OUTPUT_D
left_conveyor = ev3dev2_motor.OUTPUT_A

right = ev3dev2_motor.LargeMotor(right_port)
left = ev3dev2_motor.LargeMotor(left_port)
right_conveyor = ev3dev2_motor.MediumMotor(right_conveyor)
left_conveyor = ev3dev2_motor.MediumMotor(left_conveyor)
tank = ev3dev2_motor.MoveTank(left_port, right_port)
tank.gyro = ev3dev2_sensor.GyroSensor()

speed = Speed(40,10)
wheel = Circle(diameter=68.8)
driver = Driver(tank, speed, wheel, Circle(0))
driver.drive(1000)
#driver.turn_to(90)
path = [(3, 3), (2, 3), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (7, 7)]
driver.follow_path(path)


#tank.on_for_rotations(speed, speed, rotations)
#tank.on_for_rotations(speed, speed, rotations)
#tank.on_for_rotations(speed, speed, -rotations)

exit(0)


'''
  while True:
        command = input()
        if command == "exit":
            break

        if command == "w":
            #left_wheel.run_forever(speed_sp=200)
            #right_wheel.run_forever(speed_sp=200)
            tank.on(200,200)
        if command == "b":
            left_wheel.run_forever(speed_sp=-200)
            right_wheel.run_forever(speed_sp=-200)
        elif command == "d":
            left_wheel.run_forever(speed_sp=200)
            right_wheel.run_forever(speed_sp=-200)
        elif command == "a":
            left_wheel.run_forever(speed_sp=-200)
            right_wheel.run_forever(speed_sp=200)
        elif command == "s":
            left_wheel.stop()
            right_wheel.stop()
'''