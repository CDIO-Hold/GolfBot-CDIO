from Camera import Camera
from GolfBot.Server.Navigation import Grid, PathFinder
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
    grid = Grid(picture.width, picture.height)
    if "wall" in keyed_groups:
        for wall_box in detected_group_to_shapes(keyed_groups["wall"]):
            grid.add_box(wall_box, "wall")

    if "cross" in keyed_groups:
        for cross_box in detected_group_to_shapes(keyed_groups["cross"]):
            grid.add_box(cross_box, "wall")

    if "egg" in keyed_groups:
        for egg_box in detected_group_to_shapes(keyed_groups["egg"]):
            grid.add_box(egg_box, "egg")

    if "ball" in keyed_groups:
        shapes = detected_group_to_shapes(keyed_groups["ball"])

        for i in range(len(shapes)):
            ball_box = shapes[i]
            name = keyed_groups["ball"].objects[i].name
            grid.add_box(ball_box, name)
            grid.add_endpoint()

    if "robot" in keyed_groups:
        shapes = detected_group_to_shapes(keyed_groups["robot"])
        if len(shapes) == 1:
            robot_shape = shapes[0]
            robot_box = robot_shape.shape
            robot_angle = robot_shape.angle

            # robot.update_info(robot_box.get_center(), robot_angle.get_value(signed=True, unit=degrees))
            grid.add_box(robot_box, "robot")

    pathfinder = PathFinder(grid)

    # robot_info = robot.get_info()
    # position = robot_info.split(" ")[0]
    # x, y = (float(p) for p in position)
    grid = grid.scaled_to(picture.width//10, picture.height//10)
    print(grid)
    break
