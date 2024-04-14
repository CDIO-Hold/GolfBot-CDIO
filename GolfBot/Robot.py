from GolfBot.Direction import Direction
from GolfBot.Driver import Driver
from GolfBot.Position import Position


class Robot:
    def __init__(self, driver: Driver, position: Position, facing, ball_count: int, is_moving: bool):
        self.driver = driver
        self.position = position
        self.facing = Direction
        self.ball_count = ball_count
        self.is_moving = is_moving
