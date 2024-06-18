from Position import Position


class Box:
    def __init__(self, top_left: Position, bottom_right: Position):
        self.top_left = top_left
        self.bottom_right = bottom_right

    @property
    def x1(self) -> float:
        return self.top_left.x

    @property
    def y1(self) -> float:
        return self.top_left.y

    @property
    def x2(self) -> float:
        return self.bottom_right.x

    @property
    def y2(self) -> float:
        return self.bottom_right.y

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def dimensions(self) -> (float, float):
        return self.width, self.height
