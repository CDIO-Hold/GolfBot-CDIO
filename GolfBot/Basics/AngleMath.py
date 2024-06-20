import math
from GolfBot.Basics import Angle, radians


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