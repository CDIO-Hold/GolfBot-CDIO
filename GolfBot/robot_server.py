from Robot import Robot
from Basics import ConnectionInfo, DriveSpeed, Vector
from socket import socket, AF_INET, SOCK_DGRAM

localhost = "127.0.0.1"
port = 8000
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((localhost, port))

info = ConnectionInfo("192.168.116.17", 18812)
drive_speed = DriveSpeed(40, 10)

print("Initializing robot...")
robot = Robot(info, drive_speed, 40)
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
    elif action == "update_robot_pos":
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