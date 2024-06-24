from GolfBot.Server.ImageRecognition import DetectedObject


class DetectedGroup:
    def __init__(self, name: str):
        self.name = name
        self.objects = list()

    def add(self, obj: DetectedObject):
        self.objects.append(obj)

    @property
    def is_empty(self) -> bool:
        return len(self.objects) == 0

    def __len__(self):
        return len(self.objects)
