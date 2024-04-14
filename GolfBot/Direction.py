from GolfBot.CardinalDirection import CardinalDirection


class Direction:
    def __init__(self, angle: float):
        self.angle = angle

    def get_cardinal(self) -> CardinalDirection:
        if 45 <= self.angle < 135:
            return CardinalDirection.NORTH
        elif 135 <= self.angle < 225:
            return CardinalDirection.WEST
        elif 225 <= self.angle < 315:
            return CardinalDirection.SOUTH
        else:
            return CardinalDirection.EAST
