from .Box import Box
from .Vector import Vector


class Wall(Box):
    def __init__(self, name, start_position: Vector, end_position: Vector):
        self.name = name
        self.is_left_wall = False
        self.is_right_wall = False
        super().__init__(start_position, end_position)
