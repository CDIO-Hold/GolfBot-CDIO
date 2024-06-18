import math

from Robot import Robot
from DriveSpeed import DriveSpeed
from ConnectionInfo import ConnectionInfo
from Position import Position
from Angle import Angle, degrees
from Vector import Vector

info = ConnectionInfo("192.168.124.17", 18812)
drive_speed = DriveSpeed(40, 10)

print("Initializing robot...")
robot = Robot(info, drive_speed, 50)
print("Robot initialized")

# robot.driver.drive(1000)
# robot.driver.turn_to(90)

robot.collector.stop()
robot.driver.stop()

robot.collector.start_loading()
robot.drive_to(Position(1000, 0))
robot.collector.stop()
robot.drive_to(Position(0, 0))
robot.collector.start_unloading()

robot.driver.turn(Angle(90, degrees))
robot.collector.stop()

exit(0)


path = [(3, 3), (2, 3), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (7, 7), (3, 3)]
path = [Position(point[0], point[1]) for point in path]

# exit(0)

for i, point in enumerate(path):
    if i % 2 == 0:
        robot.collector.start_loading()
    else:
        robot.collector.start_unloading()

    x, y = point
    target = Position(x * 100, y * 100)
    print("Moving to " + str(target))
    robot.drive_to(target)

robot.collector.stop()
