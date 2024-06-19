from GolfBot.Navigation import Grid
from GolfBot.YOLO import Yolo


class Connector:
    def __init__(self,yolo: Yolo, grid: Grid):
        self.yolo = yolo
        self.grid = grid
    def run(self):

