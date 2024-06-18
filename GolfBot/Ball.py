from Position import Position


class Ball:
    def __init__(self, name, position: Position, size: int = 1):
        self.name = name
        self.position = position
        self.size = size
