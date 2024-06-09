class Position:
    def __init__(self, x, y, angle=None):
        self.x = x
        self.y = y
        self.angle = angle

    @property
    def has_angle(self):
        return self.angle is not None

    def __str__(self):
        return "(" + str(self.x) +"; " + str(self.y) + ")"
