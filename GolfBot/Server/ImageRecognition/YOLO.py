import math
from ultralytics import YOLO
import cv2
import cvzone
from GolfBot.Server.Basics import Vector, Box, CardinalDirection, AngleMath
import os
from GolfBot.Server.ImageRecognition import DetectedObject, DetectedGroup, Image


class Yolo:

    def __init__(self):
        current_directory = os.path.dirname(__file__)
        model_path = os.path.join(current_directory, 'YOLO_FINAL_MODEL.pt')
        self.model = YOLO(model_path)  # NEWEST model

        self.className = ['cross', 'egg', 'goal', 'orange-ball', 'robot', 'robot-front', 'wall', 'white-ball']

    def find_objects(self, image: Image) -> list:
        detected_objects = list()
        results = self.model(image.data, save=True)

        for result in results:
            boxes = result.boxes
            for yolo_box in boxes:
                x1, y1, x2, y2 = yolo_box.xyxy[0]
                top_left = Vector(x1, y1)
                bottom_right = Vector(x2, y2)

                bounds = Box(top_left, bottom_right)
                #cvzone.cornerRect(image.data, (bounds.x1, bounds.y1, bounds.width, bounds.height))

                # Confidence level for detected object
                confidence = math.ceil((yolo_box.conf[0] * 100)) / 100

                object_detected = int(yolo_box.cls[0])
                current_class = self.className[object_detected]

                obj = DetectedObject(current_class, bounds)
                detected_objects.append(obj)

                # Shows class name and confidence on screen
                text = f'{obj.name} {confidence:.2f}% start={x1, y1} end={x2, y2}'
                #cvzone.putTextRect(image.data, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)

        group_names = ["ball", "wall", "robot", "cross", "egg"]
        groups = {name: DetectedGroup(name) for name in group_names}

        for obj in detected_objects:
            for group_name in group_names:
                if group_name in obj.name:
                    groups[group_name].add(obj)
                    break

        # Display the image
        cv2.imshow("image", image.data)

        # Get just the values in a list
        return [groups[key] for key in groups]
