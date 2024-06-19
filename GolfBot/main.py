from Robot import Robot
from Basics import ConnectionInfo, DriveSpeed, Vector

info = ConnectionInfo("192.168.124.17", 18812)
drive_speed = DriveSpeed(40, 10)

print("Initializing robot...")
robot = Robot(info, drive_speed, 100)
print("Robot initialized")

robot.reverse_to(Vector(0, -100))
exit(0)

while True:
    print("Current location:", robot.position)
    print("Facing:", robot.facing)
    action = input("What to do now?\n")

    if action == "exit":
        break

    if action.startswith("goto"):
        x, y = action.split(" ")[1].split(",")
        target = Vector(int(x), int(y))
        robot.drive_to(target)
    elif action == "collect":
        robot.collector.start_loading()
    elif action == "shoot":
        robot.collector.start_unloading()
    elif action == "stop":
        robot.collector.stop()

robot.driver.stop()
robot.collector.stop()
exit(0)

for _ in range(3):
    robot.turn_to(Angle(50, percent))
    robot.turn_to(Angle(75, percent))
    robot.turn_to(Angle(0, percent))
    robot.turn_to(Angle(25, percent))

exit(0)

robot.collector.stop()
robot.driver.stop()

robot.collector.start_loading()
robot.drive_to(Vector(1000, 0))
robot.collector.stop()
robot.drive_to(Vector(0, 0))
robot.collector.start_unloading()

robot.driver.turn(Angle(90, degrees))
robot.collector.stop()

exit(0)


path = [(3, 3), (2, 3), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (7, 7), (3, 3)]
path = [Vector(point[0], point[1]) for point in path]

# exit(0)

for i, point in enumerate(path):
    if i % 2 == 0:
        robot.collector.start_loading()
    else:
        robot.collector.start_unloading()

    x, y = point
    target = Vector(x * 100, y * 100)
    print("Moving to " + str(target))
    robot.drive_to(target)

robot.collector.stop()
