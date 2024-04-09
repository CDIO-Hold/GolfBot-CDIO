import math
from ultralytics import YOLO
import cv2
import cvzone

#1 if more webcams, 0 if only one cam
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)

#Using someone elses data for now, will be creating our own
#Using YOLOv8l, might change to YOLOv8x, since it is more accurate

model = YOLO('bane.pt')


#objects = ['white-ball', 'orange-ball', 'wall', 'goal', 'robot', 'egg']
className = ['orange', 'robot', 'robot-front', 'white']

while True:
    success, img = cap.read()
    result = model(img, stream=True)
    for r in result:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            w, h = x2 - x1, y2 - y1
            boundedBox = int(x1), int(y1), int(w), int(h)
            cvzone.cornerRect(img, boundedBox)

            confidence = math.ceil((box.conf[0]*100))/100
            #This is for only confidence
            # cvzone.putTextRect(img, f'{confidence:.2f}%', (x1, y1-20))


            object = int(box.cls[0])
            currentClass = className[object]

            # Shows class name and confidence on screen
            text = ""
            if currentClass == "white" or currentClass == "orange":
                # Center coords
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                text = f'{className[object]} {confidence:.2f}% x={x} y={y}'
            else:
                text = f'{className[object]} {confidence:.2f}%'

            cvzone.putTextRect(img, text, (max(0, x1), max(35, y1)), scale=1,thickness=1)
    cv2.imshow("image", img)
    cv2.waitKey(1)





