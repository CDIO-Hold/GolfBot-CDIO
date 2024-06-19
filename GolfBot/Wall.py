from Basics import Vector


class Wall:
    def __init__(self, name, start_position: Vector, end_position: Vector):
        self.name = name
        self.start_position = start_position
        self.end_position = end_position
        self.is_left_wall = False
        self.is_right_wall = False
