from enum import Enum


class CardinalDirection(Enum):
    EAST = 1
    NORTH = 2
    WEST = 3
    SOUTH = 4

    @staticmethod
    def angle_to_cardinal(angle):
        if 45 <= angle < 135:
            return CardinalDirection.NORTH
        elif -45 <= angle < 45:
            return CardinalDirection.EAST
        elif angle >= 135 or angle < -135:
            return CardinalDirection.WEST
        else:
            return CardinalDirection.SOUTH
