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

        self.grid = self.grid.scaled_to(127, 72)
        print(self.grid)
        pathfinder = PathFinder(self.grid)
        exit(0)
        has_goal = False
        # has_white_ball = False
        for obj in self.yolo.detected_objects:
            if obj['type'] == 'goal':
                has_goal = True
            #elif obj['type'] == 'white-ball':
                # has_white_ball = True

        start_position = (0, 0)  # Robot's position
        end_position = None
        #if has_white_ball:
            #end_position = pathfinder.find_nearest_ball(start_position)
        if has_goal:
            end_position = pathfinder.find_nearest_goal(start_position)

        if end_position:
            print('found the position: ' + str(end_position))

            path = pathfinder.find_path(start_position, end_position)
            print(path)
        else:
            print('No goal or ball found.')
            print(self.grid)
        print(self.grid)