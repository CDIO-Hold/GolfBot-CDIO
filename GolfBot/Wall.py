from GolfBot.Position import Position


class Wall:
    def __init__(self, name, start_position: Position, end_position: Position):
        self.name = name
        self.start_position = start_position
        self.end_position = end_position
