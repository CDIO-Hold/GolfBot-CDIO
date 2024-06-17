import math
from ultralytics import YOLO
import cv2
import cvzone
from GolfBot.Shared import Ball, Egg, Position, Box, Wall, CardinalDirection, Goal
from GolfBot.Robot.Robot import Robot


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

    def detect_ball(self, class_name, x1, x2, y1, y2) -> Ball:
        # Center coords
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return Ball(class_name, Position(x, y))

    def detect_wall(self, class_name, x1, x2, y1, y2) -> Wall:
        wall = Wall(class_name, start_position=Position(x1, y1), end_position=Position(x2, y2))

        wall.is_left_wall = x1 < 640
        wall.is_right_wall = x2 > 640
        return wall

    def detect_robot(self, robot, x1, x2, y1, y2) -> Robot:
        position = Box(x1, y1, x2, y2)

        if robot is None:
            ball_count = 0
            is_moving = False
            robot = Robot(None, position, None, ball_count, is_moving)
        else:
            robot.position = position

        return robot

    def detect_robot_front(self, robot, x1, x2, y1, y2):
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        # Center of the robots coords
        robot_x = (robot.position.x1 + robot.position.x2) / 2
        robot_y = (robot.position.y1 + robot.position.y2) / 2

        # calculate the angle
        angle = math.degrees(math.atan2(y - robot_y, x - robot_x))
        direction = CardinalDirection(angle)
        robot.facing = direction

        return robot

    def detect_goal(self, name, x1, x2, y1, y2) -> Goal:
        # Center coords
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        position = Position(x, y)

        # Check if the goal is on left or right wall
        return Goal(name, position, 3)

    def goal_on_wall(self, wall):
        x = (wall.start_position.x + wall.end_position.x) / 2
        y = (wall.start_position.y + wall.end_position.y) / 2
        position = Position(x, y)

        return Goal('goal', position, 3)

    def detect_egg(self, class_name, x1, x2, y1, y2) -> Egg:
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        return Egg(self, class_name, Position(x, y))

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
                        currentBall = self.detect_ball(current_class, x1, x2, y1, y2)
                        text = f'{current_class} {confidence:.2f}% x={currentBall.position.x} y={currentBall.position.y}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    elif current_class == "wall":
                        current_wall = self.detect_wall(current_class, x1, x2, y1, y2)
                        text = f'{current_class} {confidence:.2f}% start={current_wall.start_position.x, current_wall.start_position.y} end={current_wall.end_position.x2, current_wall.end_position.y2}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                        if current_wall.is_left_wall or current_wall.is_right_wall:
                            goal = self.goal_on_wall(current_wall)
                            text = f'{current_class} {confidence:.2f}% x,y'
                            cvzone.putTextRect(img, text, (max(0, goal.position.x), max(35, goal.position.y)), scale=1,
                                               thickness=1)

                    elif current_class == "robot":
                        robot = self.detect_robot(self.robot, x1, x2, y1, y2)

                    elif current_class == "robot-front":
                        if self.robot is not None:
                            robot = self.detect_robot_front(self.robot, x1, x2, y1, y2)
                            text = f'{current_class} {confidence:.2f}% angle={robot.facing.angle:.2f}'
                            cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)
                    elif current_class == "egg":
                        egg = self.detect_egg(current_class, x1, x2, y1, y2)
                        text = f'{current_class} {confidence:.2f}% x={egg.position.x} y={egg.position.y}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

            cv2.imshow("image", img)
            cv2.waitKey(1)