from Shapes import Box


class DetectedObject:
    def __init__(self, name: str, bounding_box: Box):
        self.name = name
        self.bounding = bounding_box


class DetectedGroup:
    def __init__(self, name: str):
        self.name = name
        self.objects = list()

    def add(self, obj: DetectedObject):
        self.objects.append(obj)

    def get_by_name(self, object_name: str):
        for obj in self.objects:
            if obj.name == object_name:
                return obj
        return None

    def __getitem__(self, item):
        return self.objects[item]

    @property
    def is_empty(self) -> bool:
        return len(self.objects) == 0

    def __len__(self):
        return len(self.objects)
