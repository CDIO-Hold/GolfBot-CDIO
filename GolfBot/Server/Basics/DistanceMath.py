import math


class DistanceMath:
    @staticmethod
    def real_distance(p1, p2, squared: bool = False) -> float:
        delta_x = p2.x - p1.x
        delta_y = p2.y - p1.y

        squared_distance = delta_x * delta_x + delta_y * delta_y
        if squared:
            return squared_distance
        else:
            return math.sqrt(squared_distance)

    @staticmethod
    def manhattan_distance(p1, p2) -> float:
        delta_x = p2.x - p1.x
        delta_y = p2.y - p1.y

        return abs(delta_x) + abs(delta_y)
