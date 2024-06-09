from GolfBot.Position import Position


class Wall:
    def __init__(self, name, start_position: Position, end_position: Position):
        self.name = name
        self.start_position = start_position
        self.end_position = end_position
        self.is_left_wall = False
        self.is_right_wall = False
