import math
from ultralytics import YOLO
import cv2
import cvzone
from Basics import Ball, Vector, Box, Wall, Goal, CardinalDirection, Egg, Cross, AngleMath
import os


class Yolo:

    def __init__(self):
        self.cap = None
        # 1 if more webcams, 0 if only one cam
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        current_directory = os.path.dirname(__file__)
        model_path = os.path.join(current_directory, 'YOLO_FINAL_MODEL.pt')
        self.model = YOLO(model_path)  # NEWEST model
        # model.predict("Bane.jpg", save=True)

        self.className = ['cross', 'egg', 'goal', 'orange-ball', 'robot', 'robot-front', 'wall', 'white-ball']
        self.robot = None
        self.detected_objects = []

    def add_detected_object(self, x1, y1, x2, y2, class_name):
        self.detected_objects.append({'x_min': x1, 'y_min': y1, 'x_max': x2, 'y_max': y2, 'type': class_name})

    def detect_ball(self, class_name, x1, y1, x2, y2) -> Ball:
        # Center coords
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        self.add_detected_object(x1, y1, x2, y2, class_name)
        return Ball(class_name, Vector(x, y))

    def detect_wall(self, class_name, x1, y1, x2, y2) -> Wall:
        self.add_detected_object(x1, y1, x2, y2, class_name)
        wall = Wall(class_name, start_position=Vector(x1, y1), end_position=Vector(x2, y2))

        image_center = 1280 / 2
        wall.is_left_wall = (x1 < image_center and x2 < image_center)
        wall.is_right_wall = (x1 > image_center and x2 > image_center)
        return wall

    def detect_cross(self, class_name, x1, y1, x2, y2) -> Cross:
        self.add_detected_object(x1, y1, x2, y2, class_name)
        cross_position = Box(Vector(x1, y1), Vector(x2, y2))
        return Cross(class_name, cross_position)

    #TODO: imlement so that robot is creates a robot
    def detect_robot(self, class_name, x1, y1, x2, y2) -> Box:
        position = Box(Vector(x1, y1), Vector(x2, y2))

        if self.robot is None:
            self.robot = position
            #self.robot = Robot(None, None, None, CardinalDirection.NORTH,  position)

        return self.robot

    def detect_robot_front(self, class_name, x1, y1, x2, y2) -> CardinalDirection:
        if self.robot is None:
            return None

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        # Center of the robots coords
        robot_x = (self.robot.x1 + self.robot.x2) / 2
        robot_y = (self.robot.y1 + self.robot.y2) / 2

        # calculate the angle
        angle = AngleMath.atan2(y - robot_y, x - robot_x)
        direction = CardinalDirection.angle_to_cardinal(angle)

        self.robot.facing = direction
        self.add_detected_object(x1, y1, self.robot.x2, self.robot.y2, 'robot')
        return direction

    def detect_goal(self, name, x1, y1, x2, y2) -> Goal:
        # Center coords
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        position = Vector(x, y)
        self.add_detected_object(x1, y1, x2, y2, 'goal')
        return Goal(name, position, 3)

    def goal_on_wall(self, class_name, wall):
        x = (wall.x1 + wall.x2) // 2
        y = (wall.y1 + wall.y2) // 2
        position = Vector(x, y)

        # Check if the goal is on left or right wall
        score = 1 if wall.is_left_wall else 2 if wall.is_right_wall else 0

        self.add_detected_object(wall.x1, y - 50, wall.x2, y + 50, class_name)
        print('goal coords:', x, y)
        return Goal('goal', position, score)

    def detect_egg(self, class_name, x1, y1, x2, y2) -> Egg:
        self.add_detected_object(x1, y1, x2, y2, class_name)
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        start_pos = Vector(x1, y2)
        end_pos = Vector(x2, y2)
        return Egg(class_name, Box(start_pos, end_pos))


    def run(self):
        current_directory = os.path.dirname(__file__)
        image_path = os.path.join(current_directory, 'BaneImage.jpg')
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Unable to read image at BaneImage.jpg")
            return

        result = self.model(img)

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
                    cvzone.putTextRect(img, current_class, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                elif current_class == "wall":
                    current_wall = self.detect_wall(current_class, x1, y1, x2, y2)
                    cvzone.putTextRect(img, current_class, (max(0, x1), max(35, y1)), scale=1, thickness=1)
                    if current_wall.is_left_wall or current_wall.is_right_wall:
                        goal = self.goal_on_wall('goal', current_wall)
                        cvzone.putTextRect(img, 'goal', (max(0, (x1+x2)//2), max(35, (y1+y2)//2)), scale=1, thickness=1)
                #elif current_class == "goal":
                #goal = self.detect_goal('goal', x1, y1, x2, y2)
                #cvzone.putTextRect(img, 'goal', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                elif current_class == "robot":
                    robot = self.detect_robot(current_class, x1, y1, x2, y2)
                    cvzone.putTextRect(img, current_class, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                elif current_class == "robot-front":
                    if self.robot is not None:
                        robot = self.detect_robot_front(current_class, x1, y1, x2, y2)
                        cvzone.putTextRect(img, current_class, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                elif current_class == "egg":
                    egg = self.detect_egg(current_class, x1, y1, x2, y2)
                    cvzone.putTextRect(img, current_class, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                elif current_class == "cross":
                    current_cross = self.detect_cross(current_class, x1, y1, x2, y2)
                    #cvzone.putTextRect(img, current_class, (max(0, x1), max(35, y1)), scale=1, thickness=1)
                # print('objects:' + self.detected_objects.__str__() + '\n')
            # Show the processed image
            output_image = 'BaneImg_annotated.jpg'
            # Save the annotated image
            #cv2.imwrite(output_image, img)

            #cv2.imshow('image', img)
            #cv2.waitKey(0)  # Wait for any key press
            cv2.destroyAllWindows()
            return img, self.detected_objects



    '''
    def run(self):
        while True:
            success, img = self.cap.read()
            result = self.model(img, stream=True)
            self.detected_objects.clear()
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
                        text = f'{current_class} {confidence:.2f}% start={current_wall.x1, current_wall.y1} end={current_wall.x2, current_wall.y2}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)
                        if current_wall.is_left_wall or current_wall.is_right_wall:
                            goal = self.goal_on_wall('goal', current_wall)
                            text = (
                                f'{current_class} {confidence:.2f}% x= {(current_wall.x1 + current_wall.x2) / 2}, '
                                f'y = {(current_wall.y1 + current_wall.y2) / 2}')
                            cvzone.putTextRect(img, text, (max(0, (x1 + x2 // 2)), max(35, (y1 + x2) // 2)), scale=1,
                                               thickness=1)

                    #elif current_class == "goal":
                    #goal = self.detect_goal('goal', x1, y1, x2, y2)
                    #cvzone.putTextRect(img, 'goal', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                    elif current_class == "robot-front":
                        if self.robot is not None:
                            robot = self.detect_robot_front(current_class, x1, y1, x2, y2)
                            text = f'{current_class} {confidence:.2f}% angle={robot.facing.angle:.2f}'
                            cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    elif current_class == "robot":
                        robot = self.detect_robot(current_class, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% start: ={x1:2f}%, {y1:2f}% end: ={x2:2f}%, {y2:2f}%'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    elif current_class == "egg":
                        egg = self.detect_egg(current_class, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% x={egg.position.x} y={egg.position.y}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    elif current_class == "cross":
                        current_cross = self.detect_cross(current_class, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% start={current_cross.position.x1, current_cross.position.y1} end={current_cross.position.x2, current_cross.position.y2}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)
                    #print('objects:' + self.detected_objects.__str__() + '\n')
            # Display the image
            cv2.imshow("image", img)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

            #cv2.imwrite('captured_image.jpg', img)
            #time.sleep(self.capture_interval)

            self.cap.release()
    '''
'''
    def run(self):
        #self.add_detected_object(20, 20, 10, 10, 'goal')
        success, img = self.cap.read()
        if not success:
            print("Failed to capture image")
            return None, None

        result = self.model(img, stream=True)
        self.detected_objects.clear()  #Remove the old detected objects

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
                    text = f'{current_class} {confidence:.2f}% start={current_wall.x1, current_wall.y1} end={current_wall.x2, current_wall.y2}'
                    cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)
                    if current_wall.is_left_wall or current_wall.is_right_wall:
                        goal = self.goal_on_wall('goal', current_wall)
                        text = (
                            f'{current_class} {confidence:.2f}% x= {(current_wall.x1 + current_wall.x2) / 2}, '
                            f'y = {(current_wall.y1 + current_wall.y2) / 2}')
                        cvzone.putTextRect(img, text, (max(0, (x1 + x2 // 2)), max(35, (y1 + x2) // 2)), scale=1,
                                           thickness=1)

                elif current_class == "robot-front":
                    if self.robot is not None:
                        direction = self.detect_robot_front(current_class, x1, y1, x2, y2)
                        text = f'{current_class} {confidence:.2f}% angle={direction}'
                        cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                elif current_class == "robot":
                    robot = self.detect_robot(current_class, x1, y1, x2, y2)
                    text = f'{current_class} {confidence:.2f}% start: ={x1:2f}%, {y1:2f}% end: ={x2:2f}%, {y2:2f}%'
                    cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                elif current_class == "egg":
                    egg = self.detect_egg(current_class, x1, y1, x2, y2)
                    text = f'{current_class} {confidence:.2f}% start ={egg.position.x1, egg.position.y1} end={egg.position.x2, egg.position.y2}'
                    cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

                elif current_class == "cross":
                    current_cross = self.detect_cross(current_class, x1, y1, x2, y2)
                    text = f'{current_class} {confidence:.2f}% start={current_cross.position.x1, current_cross.position.y1} end={current_cross.position.x2, current_cross.position.y2}'
                    cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

            # Display the image
        cv2.imshow("image", img)

        #self.cap.release()
        #cv2.destroyAllWindows()

        return img, self.detected_objects
'''