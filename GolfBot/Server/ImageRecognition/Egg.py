from GolfBot.Server.Basics import Box


class Egg:
    def __init__(self, name, bounding_box: Box):
        self.name = name
        self.bounding_box = bounding_box
