from Camera import Camera
from YOLO import Yolo
from Server import Server
from ScreenToWorld import ScreenToWorld
from Angle import degrees
from DetectedToModel import detected_group_to_shapes


print("Starting camera...")
camera = Camera()
print("Initializing screen to world converter...")
screen_to_world = ScreenToWorld(camera)
print("Initializing YOLO...")
yolo = Yolo()
print("Initializing server...")
server = Server()
print("Ready")
# input("Press enter to continue")

while True:
    print("Finding objects...")
    groups = yolo.find_objects(camera.take_picture())

    keyed_groups = dict()
    for group in groups:
        keyed_groups[group.name] = group

    if "robot" in keyed_groups:
        shapes = detected_group_to_shapes(keyed_groups["robot"])
        if len(shapes) == 1:
            robot_shape = shapes[0]
            robot_box = screen_to_world.convert_box(robot_shape.shape)
            robot_angle = screen_to_world.convert_angle(robot_shape.angle)

            server.update_robot(robot_box.get_center(), robot_angle.get_value(signed=True, unit=degrees))

    if "wall" in keyed_groups:
        pass

    if "cross" in keyed_groups:
        pass

    if "egg" in keyed_groups:
        pass

    if "ball" in keyed_groups:
        pass
