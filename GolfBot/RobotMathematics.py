import math
from Angle import Angle, radians
from Position import Position


class AngleMath:
    @staticmethod
    def acos(x) -> Angle:
        print("Acos of " + str(x))
        return Angle(math.acos(x), radians)

    @staticmethod
    def asin(x) -> Angle:
        return Angle(math.asin(x), radians)

    @staticmethod
    def atan(x) -> Angle:
        return Angle(math.atan(x), radians)

    @staticmethod
    def atan2(y, x) -> Angle:
        return Angle(math.atan2(y, x), radians)

    @staticmethod
    def get_radians(angle) -> float:
        if type(angle) is int or type(angle) is float:
            return angle
        else:
            return angle.get_value(signed=False, unit=radians)

    @staticmethod
    def cos(x) -> float:
        return math.cos(AngleMath.get_radians(x))

    @staticmethod
    def sin(x) -> float:
        return math.sin(AngleMath.get_radians(x))

    @staticmethod
    def tan(x) -> float:
        return math.tan(AngleMath.get_radians(x))


class DistanceMath:
    @staticmethod
    def real_distance(a: Position, b: Position, squared: bool = False) -> float:
        delta_x = b.x - a.x
        delta_y = b.y - a.y

        squared_distance = delta_x * delta_x + delta_y * delta_y
        if squared:
            return squared_distance
        else:
            return math.sqrt(squared_distance)

    @staticmethod
    def manhattan_distance(a: Position, b: Position) -> float:
        delta_x = b.x - a.x
        delta_y = b.y - a.y

        return abs(delta_x) + abs(delta_y)
