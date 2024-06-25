from Camera import Camera
from GolfBot.Server.Navigation import Grid, PathFinder
from YOLO import Yolo
from RobotClient import RobotClient
from Vector import Vector
from Angle import degrees
from Shapes import Box
from DetectedToModel import detected_group_to_shapes
from LastMinute import *


print("Starting camera...")
camera = Camera(0)
print("Initializing YOLO...")
yolo = Yolo()
print("Initializing server...")
robot = RobotClient()
print("Ready")
# input("Press enter to continue")
robot.connect("127.0.0.1", 8000)

screen_to_world = ScreenToWorld()

goals = dict()
while True:
    print("Finding objects...")
    picture = camera.take_picture()

    if picture.data is None:
        print("Error while taking the picture. Trying again...")
        continue

    groups = yolo.find_objects(picture)
    keyed_groups = dict()
    for group in groups:
        if not group.is_empty:
            keyed_groups[group.name] = group

    # initialize grid
    field = Field()

    if "wall" in keyed_groups:
        walls = []
        for wall_box in detected_group_to_shapes(keyed_groups["wall"]):
            walls.append(wall_box)

        screen_to_world.calibrate_from_walls(walls)

    if "cross" in keyed_groups:
        cross_box = detected_group_to_shapes(keyed_groups["cross"])[0]
        field.insert_cross(cross_box.get_center(), screen_to_world)

    if "egg" in keyed_groups:
        egg_box = detected_group_to_shapes(keyed_groups["egg"])[0]
        field.insert_egg(egg_box.get_center(), screen_to_world)

    if "ball" in keyed_groups:
        shapes = detected_group_to_shapes(keyed_groups["ball"])

        for i in range(len(shapes)):
            ball_box = shapes[i]
            name = keyed_groups["ball"].objects[i].name
            color = name.split("-")[0]

            field.insert_ball(ball_box.get_center(), color, screen_to_world)

    if "robot" in keyed_groups:
        shapes = detected_group_to_shapes(keyed_groups["robot"])
        if len(shapes) == 1:
            robot_shape = shapes[0]
            robot_box = screen_to_world.box(robot_shape.shape)
            robot_angle = robot_shape.angle * -1

            print("Updating robot position")
            robot.update_info(robot_box.get_center(), robot_angle.get_value(signed=True, unit=degrees))

    robot_info = robot.get_info()
    position = robot_info.split(" ")[0]
    x, y = (int(p.split(".")[0]) for p in position.split(","))

    balls = field.get_seen_balls(Vector(x, y))
    print([(str(ball.get_center()), ball.color) for ball in balls])
