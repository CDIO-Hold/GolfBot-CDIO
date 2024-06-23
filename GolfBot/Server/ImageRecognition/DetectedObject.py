from GolfBot.Server.Basics import Box


class DetectedObject:
    def __init__(self, name: str, bounding_box: Box):
        self.name = name
        self.bounding = bounding_box
