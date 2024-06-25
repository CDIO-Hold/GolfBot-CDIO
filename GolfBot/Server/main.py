from Camera import Camera, Image
from GolfBot.Server.Navigation import Grid, PathFinder
from YOLO import Yolo
from RobotClient import RobotClient, ScreenToWorld
from Vector import Vector
from Angle import degrees
from Shapes import Box
from DetectedToModel import detected_group_to_shapes


print("Starting camera...")
camera = Camera(0)
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
radius = int(150 // scale) + 1
print("Initializing server...")
screen_to_world = ScreenToWorld(camera, scale=scale)
robot = RobotClient(screen_to_world)
print("Ready")
# input("Press enter to continue")

robot.connect("127.0.0.1", 8000)

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
        keyed_groups[group.name] = group

    # initialize grid
    grid = Grid(picture.width, picture.height)

    if "wall" in keyed_groups:
        walls = []
        for wall_box in detected_group_to_shapes(keyed_groups["wall"]):
            grid.add_box(wall_box, "wall")
            walls.append(wall_box)
        left_and_right = sorted(walls, key=lambda box: box.width)[:2]

        left, right = sorted(left_and_right, key=lambda box: box.get_center().x)

        # Add the goals
        left_goal_width = 200 * scale
        left_center = left.get_center()
        left_goal = Box(Vector(left.x1, left_center.y - (left_goal_width // 2)), Vector(left.x2, left_center.y + (left_goal_width // 2)))
        # grid.add_endpoint(left_goal.get_center(), "goal", safe_zone=0)

        right_goal_width = 80 * scale
        right_center = right.get_center()
        right_goal = Box(Vector(right.x1, right_center.y - (right_goal_width // 2)), Vector(right.x2, right_center.y + (right_goal_width // 2)))
        # grid.add_endpoint(right_goal.get_center(), "goal", safe_zone=0)

        left_goal_endpoint = {
            'center': left_goal.get_center().as_tuple(),
            'staggered': None,
            'type': 'goal'
        }
        right_goal_endpoint = {
            'center': right_goal.get_center().as_tuple(),
            'staggered': None,
            'type': 'goal'
        }

        goals['left'] = left_goal_endpoint
        goals['right'] = right_goal_endpoint

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
            grid.add_endpoint(ball_box.get_center(), name, radius)

    if "robot" in keyed_groups:
        shapes = detected_group_to_shapes(keyed_groups["robot"])
        if len(shapes) == 1:
            robot_shape = shapes[0]
            robot_box = robot_shape.shape
            robot_angle = robot_shape.angle

            print("Updating robot position")
            robot.update_info(robot_box.get_center(), robot_angle.get_value(signed=True, unit=degrees))
            grid.add_box(robot_box, "robot")
    pathfinder = PathFinder(grid)
    print(grid.scaled_to(128, 72))
    robot_info = robot.get_info()
    position = robot_info.split(" ")[0]
    x, y = (int(p.split(".")[0]) for p in position.split(","))
    grid.sorted_end_points((x, y))
    print('Endpoints: ')
    print(grid.end_points)

    if len(grid.end_points) > 0:
        path = pathfinder.find_path((x, y), grid.end_points[0])
        print(f"Rute givet: {path}")
        type = grid.end_points[0]['type']
    else:
        print(f'Kører til mål ({goals["left"]["center"]})')
        path = pathfinder.find_path((x, y), goals['left'])

    print("Starting collection")
    robot.collect()
    for position in path:
        x, y = position
        robot.move_to(Vector(x, y))

    # break
