from Camera import Camera
from YOLO import Yolo
from DetectedToModel import detected_group_to_shapes


print("Starting camera...")
camera = Camera()
print("Initializing YOLO...")
yolo = Yolo()
print("Ready")

print("Finding objects...")
groups = yolo.find_objects(camera.take_picture())
print("Found:")
print(len(groups), groups)

for group in groups:
    if group.is_empty:
        print(f"{group.name} is empty")
    else:
        print(f"{group.name} has {len(group)} members")
        shapes = detected_group_to_shapes(group)
        print(f"Resulting shapes: {[str(shape) for shape in shapes]}")
