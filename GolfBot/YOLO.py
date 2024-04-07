from ultralytics import YOLO

model = YOLO('yolov8x')

model.predict("Bane.jpg", save=True)






