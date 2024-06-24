from Camera import Camera
from GolfBot.Server.Navigation import Grid
from YOLO import Yolo
from RobotClient import RobotClient
from ScreenToWorld import ScreenToWorld
from Angle import degrees
from DetectedToModel import detected_group_to_shapes


server = RobotClient()
print("Ready")
# input("Press enter to continue")
server.connect("127.0.0.1", 8000)

while True:
    command = input("Enter command: ")
    if command == "exit":
        server.close()
        break

    answer = server.send(command)
    print(f"[SERVER]: {answer}")
