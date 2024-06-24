from Camera import Camera
from GolfBot.Server.Navigation import Grid
from YOLO import Yolo
from RobotClient import RobotClient, ScreenToWorld
from Angle import degrees
from DetectedToModel import detected_group_to_shapes


print("Starting camera...")
camera = Camera()
print("Initializing YOLO...")
yolo = Yolo()
print("Figuring out the scale")
scale = 1.0
real_ball_size = 40  # mm
while True:
    print("Taking a picture")
    picture = camera.take_picture()
    if picture.data is None:
        continue

    print("Finding a ball")
    groups = yolo.find_objects(picture)

    ball_group = None
    for group in groups:
        if group.name == "ball":
            ball_group = group
            break

    if ball_group is None or ball_group.is_empty:
        continue

    balls = detected_group_to_shapes(ball_group)
    screen_ball_size = max(balls[0].width, balls[0].height)
    scale = real_ball_size / screen_ball_size
    break

print("Initializing server...")
screen_to_world = ScreenToWorld(camera, scale=scale)
robot = RobotClient(screen_to_world)
print("Ready")
# input("Press enter to continue")
robot.connect("127.0.0.1", 8000)
while True:
    print("Finding objects...")
    picture = camera.take_picture()

    if picture.data is None:
        print("Error while taking the picture. Trying again...")
        continue

    groups = yolo.find_objects(picture)

    keyed_groups = dict()
    for group in groups:
        keyed_groups[group.name] = group

    # initialize grid
    # grid = Grid(picture.width, picture.height)

    if "robot" in keyed_groups:
        shapes = detected_group_to_shapes(keyed_groups["robot"])
        if len(shapes) == 1:
            robot_shape = shapes[0]
            robot_box = robot_shape.shape
            robot_angle = robot_shape.angle

            robot.update_info(robot_box.get_center(), robot_angle.get_value(signed=True, unit=degrees))


    if "wall" in keyed_groups:
        pass

    if "cross" in keyed_groups:
        shapes = detected_group_to_shapes(keyed_groups["cross"])
        if len(shapes) == 2:
            cross_shape = shapes[0]

            cross_box = cross_shape.shape



    if "egg" in keyed_groups:
        pass

    balls = [] if "ball" not in keyed_groups else detected_group_to_shapes(keyed_groups["ball"])

    if len(balls) > 0:
        print("found a target")
        target = balls[0]
        print("started collect...")
        robot.collect()
        print("sending coords")
        robot.move_to(target.get_center())
        print("coords sent: " + str(target.get_center()))

    print(f"Robot: {robot.get_info()}")
