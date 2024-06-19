from .Driver import Driver
from .Collector import Collector
from ..Shared import Box_Position


class Robot:
    def __init__(self, driver: Driver, collector: Collector, position: Box_Position, size, facing):
        self.driver = driver
        self.collector = collector
        self.position = position
        self.size = size
        self.facing = facing
