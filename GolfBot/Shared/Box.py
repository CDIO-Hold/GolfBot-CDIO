from Position import Position

class Box:
    def __init__(self, top_left: Position, bottom_right: Position):
        self.top_left = top_left
        self.bottom_right = bottom_right

    @property
    def x1(self):
        return self.top_left.x

    @property
    def y1(self):
        return self.top_left.y

    @property
    def x2(self):
        return self.bottom_right.x

    @property
    def y2(self):
        return self.bottom_right.y
