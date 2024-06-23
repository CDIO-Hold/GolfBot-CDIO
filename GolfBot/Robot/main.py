from socket import socket, AF_INET, SOCK_DGRAM
import rpyc
from Circle import Circle
from Vector import Vector
from Collector import Collector
from Driver import Driver
from Robot import Robot

# Make a socket to connect with the image recognition & pathfinding programs
localhost = "127.0.0.1"
port = 8000
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((localhost, port))

# Make the connection to the robot through rpyc
robot_ip = "192.168.124.17"
robot_port = 18812
robot_connection = rpyc.classic.connect(robot_ip, robot_port)
ev3_motors = robot_connection.modules['ev3dev2.motor']

# Hardcoded values, found by looking at the robot wires
left_wheel = ev3_motors.OUTPUT_B
right_wheel = ev3_motors.OUTPUT_C
left_conveyor = ev3_motors.OUTPUT_D
right_conveyor = ev3_motors.OUTPUT_A

# Construct driver
drive_steering = ev3_motors.MoveSteering(left_wheel, right_wheel, motor_class=ev3_motors.LargeMotor)
straight_speed = 40
turn_speed = 10
wheel = Circle(diameter=68.8)
wheel_distance = 111
turn_circle = Circle(diameter=wheel_distance)
driver = Driver(drive_steering, straight_speed, turn_speed, wheel, turn_circle)

# Construct collector
conveyor_steering = ev3_motors.MoveSteering(left_conveyor, right_conveyor, motor_class=ev3_motors.MediumMotor)
collector = Collector(conveyor_steering, 40)

print("Initializing robot...")
robot = Robot(driver, collector)
print("Robot initialized")

while True:
    print("Current location:", robot.position)
    print("Facing:", robot.facing)
    data, sender = sock.recvfrom(1024)
    action = data.decode("utf-8")
    answer = b'Accepted'
    if action == "exit":
        break

    if action.startswith("goto"):
        target = action.split(" ")[1]
        x, y = target.split(",")
        target = Vector(int(x), int(y))
        robot.drive_to(target)
    elif action == "collect":
        robot.collector.start_loading()
    elif action == "shoot":
        robot.collector.start_unloading()
    elif action.startswith("update_robot_pos"):
        target = action.split(" ")[1]
        x, y = target.split(",")
        target = Vector(int(x), int(y))
        robot.set_position(target)
    elif action == "stop":
        robot.collector.stop()

    else:
        answer = b"Unknown command"

    sock.sendto(answer, sender)

robot.driver.stop()
robot.collector.stop()

print("Shutting down server")
sock.close()
