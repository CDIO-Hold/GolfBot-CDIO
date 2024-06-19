from GolfBot.Navigation import Grid
from GolfBot.Navigation.PathFinder import PathFinder
from GolfBot.YOLO import Yolo


class Connector:
    def __init__(self, yolo: Yolo, grid: Grid):
        self.yolo = yolo
        self.grid = grid

    def run(self):
        self.yolo.run()

        detected_objs = self.yolo.detected_objects
        print("Detected_objs: " + str(detected_objs))

        self.grid.add_detected_object(detected_objs)
        self.grid.add_object(0, 0, 6)  # starting position

        pathfinder = PathFinder(self.grid)

        has_goal = False
        has_white_ball = False
        for obj in self.yolo.detected_objects:
            if obj['type'] == 'goal':
                goal = True
            elif obj['type'] == 'white-ball':
                has_white_ball = True
        end_position = (0, 0)
        if has_white_ball:
            end_position = pathfinder.find_nearest_ball((0, 0))
        elif has_goal:
            end_position = pathfinder.find_nearest_goal((0, 0))

        print('found the position' + str(end_position))

        path = pathfinder.find_path((0, 0), end_position)
        print(path)
