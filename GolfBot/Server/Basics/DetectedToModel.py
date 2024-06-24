from GolfBot.Server.Basics import Vector, Shape, Box, AngledShape, MultiShape
from GolfBot.Server.ImageRecognition import DetectedGroup, DetectedObject


def detected_group_to_shapes(group: DetectedGroup) -> list[Shape | AngledShape]:
    if group.name == "robot":
        if len(group) != 2:
            # Either a part of the robot is missing, or something is wrongly categorized
            return []
        front = group.get_by_name("robot-front")
        back = group.get_by_name("robot")

        if front is None or back is None:
            return []

        robot_x1 = min(back.bounding.x1, front.bounding.x1)
        robot_y1 = min(back.bounding.y1, front.bounding.y1)
        robot_x2 = max(back.bounding.x2, front.bounding.x2)
        robot_y2 = max(back.bounding.y2, front.bounding.y2)

        robot_top_left = Vector(robot_x1, robot_y1)
        robot_bottom_right = Vector(robot_x2, robot_y2)

        robot_bounds = Box(robot_top_left, robot_bottom_right)

        back_position = back.bounding.get_center()
        front_position = front.bounding.get_center()
        robot_vector = Vector.from_points(back_position, front_position)

        robot_shape = AngledShape(robot_bounds, robot_vector.angle)
        return [robot_shape]

    if group.name == "cross":
        if len(group) != 2:
            # The cross should always have exactly 2 parts
            return []

        cross_shape = MultiShape(group[0], group[1])
        return [cross_shape]

    shapes = list()
    if group.name == "wall":
        pass  # Goals?

    for obj in group.objects:
        shapes.append(obj)
    return shapes
