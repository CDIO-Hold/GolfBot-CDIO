from GolfBot.Direction import Direction
from GolfBot.Driver import Driver
from GolfBot.Box import Box


class Robot:
    def __init__(self, driver: Driver, position: Box, facing: Direction, ball_count: int, is_moving: bool):
        self.driver = driver
        self.position = position
        self.facing = facing
        self.ball_count = ball_count
        self.is_moving = is_moving