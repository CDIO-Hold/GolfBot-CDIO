import math
from ultralytics import YOLO
import cv2
import cvzone
from GolfBot.Ball import Ball
from GolfBot.Wall import Wall

# 1 if more webcams, 0 if only one cam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Using YOLOv8l, might change to YOLOv8x, since it is more accurate
#model = YOLO('bane.pt') #Balls detection
model = YOLO('field.pt') #Balls and walls

#model.predict("Bane.jpg", save=True)

# className = ['white-ball', 'orange-ball', 'wall', 'goal', 'robot','robot_front', 'egg']
#className = ['Back', 'robot', 'robot-front', 'white']  #Balls
className = ['Back', 'Ball orange', 'Ball white', 'Bounds', 'Corner', 'Cross', 'Front', 'Robot'] # Balls and walls

def detect_ball(class_name, x1, x2, y1, y2) -> Ball:
    # Center coords
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    return Ball(class_name, x, y)

def detect_wall(class_name, x1, x2, y1, y2) -> Wall:
    #start = (x1, y2)
    #end = (x2, y2)

    return Wall(class_name, x1, y2, x2, y2)

while True:
    success, img = cap.read()
    result = model(img, stream=True)
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
            current_class = className[object_detected]

            # Shows class name and confidence on screen
            text = ""
            #if current_class == "white" or current_class == "orange": # for balls only
            if current_class == "Ball white" or current_class == "Ball orange": #for balls and walls
                current_ball = detect_ball(current_class, x1, x2, y1, y2)
                text = f'{current_class[object_detected]} {confidence:.2f}% x={current_ball.x} y={current_ball.y}'

                cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)
            elif current_class == 'Bounds': #walls
                current_wall = detect_wall(current_class, x1, x2, y1, y2)
                text = f'{current_class[object_detected]} {confidence:.2f}% start={current_wall.x1, current_wall.y2} end={current_wall.x2, current_wall.y2}'

                cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1, thickness=1)
            elif confidence < 0.5:
                cvzone.putTextRect(img, f'{current_class[object_detected]} {confidence:.2f}%', (max(0, x1), max(35, y1)),
                                   scale=1,
                                   thickness=1)

    cv2.imshow("image", img)
    cv2.waitKey(1)
