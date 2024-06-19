import math
from ultralytics import YOLO
import cv2
import cvzone
from GolfBot.Shared import Ball, Egg, Position, Box_Position, Wall, CardinalDirection, Goal
from GolfBot.Robot.Robot import Robot
from GolfBot.Shared.Cross import Cross


class Yolo:

    def __init__(self):
        # 1 if more webcams, 0 if only one cam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        self.model = YOLO('best.pt')  # NEWEST Before 3 ugers
        # model.predict("Bane.jpg", save=True)

        self.className = ['egg', 'goal', 'orange-ball', 'robot', 'robot-front', 'wall', 'white-ball']
        self.robot = None
        self.detected_objects = []

    def add_detected_object(self, x1, y1, x2, y2, class_name):
        self.detected_objects.append({'x_min': x1, 'y_min': y1, 'x_max': x2, 'y_max': y2, 'type': class_name})

    def detect_ball(self, class_name, x1, y1, x2, y2) -> Ball:
        # Center coords
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        self.add_detected_object(x1, y1, x2, y2, class_name)
        return Ball(class_name, Position(x, y))

    def detect_wall(self, class_name, x1, y1, x2, y2) -> Wall:
        self.add_detected_object(x1, y1, x2, y2, class_name)
        wall = Wall(class_name, start_position=Position(x1, y1), end_position=Position(x2, y2))

        image_center = 1280 / 2
        wall.is_left_wall = (x1 < image_center and x2 < image_center)
        wall.is_right_wall = (x1 > image_center and x2 > image_center)
        return wall

    def detect_cross(self, class_name, x1, y1, x2, y2) -> Cross:
        self.add_detected_object(x1, y1, x2, y2, class_name)
        cross_position = Box_Position(Position(x1, y1), Position(x2, y2))
        return Cross(class_name, cross_position)

    def detect_robot(self, class_name, robot, x1, y1, x2, y2) -> Robot:
        position = Box_Position(Position(x1, y1), Position(x2, y2))

        if robot is None:
            robot = Robot(None, None, position, 1, CardinalDirection.NORTH)
        else:
            robot.position = position

        return robot

    def detect_robot_front(self, class_name, robot, x1, y1, x2, y2):
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        # Center of the robots coords
        robot_x = (robot.position.x1 + robot.position.x2) / 2
        robot_y = (robot.position.y1 + robot.position.y2) / 2

        # calculate the angle
        angle = math.degrees(math.atan2(y - robot_y, x - robot_x))
        direction = CardinalDirection.angle_to_cardinal(angle)
        robot.facing = direction
        self.add_detected_object(x1, y1, robot.position.x2, robot.position.y2, class_name)
        return robot

    def detect_goal(self, name, x1, y1, x2, y2) -> Goal:
        # Center coords
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        position = Position(x, y)

        return Goal(name, position, 3)

    def goal_on_wall(self, class_name,  wall):
        x = (wall.start_position.x + wall.end_position.x) / 2
        y = (wall.start_position.y + wall.end_position.y) / 2
        position = Position(x, y)

        # Check if the goal is on left or right wall
        score = 1 if wall.is_left_wall else 2 if wall.is_right_wall else 0
        self.add_detected_object(wall.start_position.x, wall.start_position.y, wall.end_position.x, wall.end_position.y, class_name)
        return Goal('goal', position, score)

    def detect_egg(self, class_name, x1, y1, x2, y2) -> Egg:
        self.add_detected_object(x1, y1, x2, y2, class_name)
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        
        return Egg(class_name, Position(x, y))

    def run(self):
        while True:
            success, img = self.cap.read()
            result = self.model(img, stream=True)
            for r in result:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    w, h = x2 - x1, y2 - y1
                    bounded_box = int(x1), int(y1), int(w), int(h)
                    cvzone.cornerRect(img, bounded_box)

                    # Confidence level for detected object
                    confidence = math.ceil((box.conf[0] * 100)) / 100

                    object_detected = int(box.cls[0])
                    current_class = self.className[object_detected]

                    # Shows class name and confidence on screen
                    text = ""
                    if current_class == "orange-ball" or current_class == "white-ball":
                        current_ball = self.detect_ball(current_class, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% x={current_ball.position.x} y={current_ball.position.y}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    elif current_class == "wall":
                        current_wall = self.detect_wall(current_class, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% start={current_wall.start_position.x, current_wall.start_position.y} end={current_wall.end_position.x2, current_wall.end_position.y2}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)
                        if current_wall.is_left_wall or current_wall.is_right_wall:
                            goal = self.goal_on_wall('goal', current_wall)
                            text = f'{current_class} {confidence:.2f}% x,y'
                            cvzone.putTextRect(img, text, (max(0, goal.position.x), max(35, goal.position.y)), scale=1,
                                               thickness=1)

                    elif current_class == "robot":
                        robot = self.detect_robot(current_class, self.robot, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% coords: ={robot.position.x:2f}%, {robot.position.y:2f}%'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    elif current_class == "robot-front":
                        if self.robot is not None:
                            robot = self.detect_robot_front(current_class, self.robot, x1, y1, x2, y2)
                            text = f'{current_class} {confidence:.2f}% angle={robot.facing.angle:.2f}'
                            cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    elif current_class == "egg":
                        egg = self.detect_egg(current_class, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% x={egg.position.x} y={egg.position.y}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    elif current_class == "cross":
                        current_cross = self.detect_cross(current_class, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% start={current_cross.position.top_left.x, current_cross.position.top_left.y} end={current_cross.position.bottom_right.x, current_cross.position.bottom_right.y}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

            cv2.imshow("image", img)
            cv2.waitKey(1)
