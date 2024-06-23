from GolfBot.Navigation import Grid
from GolfBot.Navigation.PathFinder import PathFinder
from GolfBot.YOLO import Yolo


class Connector:
    def __init__(self, yolo: Yolo, grid: Grid):
        self.yolo = yolo
        self.grid = grid

    def run(self):
        print("before yolo.run")
        self.yolo.run()
        print("after yolo.run")
        detected_objs = self.yolo.detected_objects
        print("Detected_objs: " + str(detected_objs))

        self.grid.add_detected_object(detected_objs)
        self.grid.add_object(0, 0, 6)  # starting position
        self.grid = self.grid.scaled_to(127, 72)
        print("Printing end points: " + str(self.grid.end_points))
        print(self.grid)
        pathfinder = PathFinder(self.grid)

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
            print("printing end points: " + str(self.grid.end_points))
            self.grid.sorted_end_points(start_position)
            print("printing end points: " + str(self.grid.end_points))
            print(self.grid.end_points[0])
            #end_position = (20, 29)
            end_position = self.grid.end_points[1]['center']
        if end_position:
            print('found the position: ' + str(end_position))
            print('Finding path between ' + str(start_position) + ' and ' + str(end_position))
            path = pathfinder.find_path(start_position, end_position)
            print(path)
            self.visualize_path(path, start_position, end_position)
        else:
            print('No goal or ball found.')
            print(self.grid)

    def visualize_path(self, path, start, goal):
        display_grid = self.grid
        for pos in path:
            display_grid.add_object(pos[0], pos[1], 2)
        display_grid.add_object(start[0], start[1], 6)
        display_grid.add_object(goal[0], goal[1], 9)
        print(display_grid)
        #print(self.grid)