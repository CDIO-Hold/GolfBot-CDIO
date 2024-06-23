from ImageRecognition import Camera, Yolo

print("Starting camera...")
camera = Camera()
print("Initializing YOLO...")
yolo = Yolo()
print("Ready")

print("Finding objects...")
objects = yolo.find_objects(camera.take_picture())
print("Found:")
print(len(objects), objects)
