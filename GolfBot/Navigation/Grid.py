import numpy as np
from queue import Queue


class Grid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.end_points = []

    def add_detected_object(self, detected_objects):
        for obj in detected_objects:
            obj_type = obj['type']
            if obj_type == "goal":
                print("adding goal")
                xmin = obj['x_min']
                xmax = obj['x_max']
                ymin = obj['y_min']
                ymax = obj['y_max']
                self.add_2d_object(xmin, xmax, ymin, ymax, 8)
                self.add_end_point(obj)
            elif obj_type == "robot":
                print("adding robot")
                center_x, center_y = self.get_center_coords(obj)
                self.add_object(center_x, center_y, 9)
                #xmin = obj['x_min']
                #xmax = obj['x_max']
                #ymin = obj['y_min']
                #ymax = obj['y_max']
                #self.add_2d_object(xmin, xmax, ymin, ymax, 9)
            elif obj_type == "white-ball":
                print("adding white-ball")
                center_x, center_y = self.get_center_coords(obj)
                self.add_object(center_x, center_y, 2)
                self.add_end_point(obj)
            elif obj_type == "orange-ball":
                print("adding orange-ball")
                center_x, center_y = self.get_center_coords(obj)
                self.add_object(center_x, center_y, 3)
                self.add_end_point(obj)
            elif obj_type == "wall":
                print("adding wall")
                xmin = obj['x_min']
                xmax = obj['x_max']
                ymin = obj['y_min']
                ymax = obj['y_max']
                self.add_2d_object(xmin, xmax, ymin, ymax, 1)
            elif obj_type == "cross":
                print("adding cross")
                xmin = obj['x_min']
                xmax = obj['x_max']
                ymin = obj['y_min']
                ymax = obj['y_max']
                self.add_2d_object(xmin, xmax, ymin, ymax, 4)
            elif obj_type == "egg":
                print("adding egg")
                xmin = obj['x_min']
                xmax = obj['x_max']
                ymin = obj['y_min']
                ymax = obj['y_max']
                self.add_2d_object(xmin, xmax, ymin, ymax, 5)

    def add_object(self, x, y, obj_type):
        x = int(x)
        y = int(y)
        if self.cell_withing_bounds(x, y):
            self.grid[y][x] = obj_type


    def add_2d_object(self, xmin, xmax, ymin, ymax, obj_type):
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                #print("i: " + str(i) + "j: " + str(j))
                if self.cell_withing_bounds(i, j):
                    self.add_object(i, j, obj_type)
    def add_end_point(self, end_point):
        end_point_obj = {'center': self.get_center_coords(end_point), 'type': end_point['type']}
        self.end_points.append(end_point_obj)


    def sorted_end_points(self, current_position):
        # Initialize lists to store white balls, orange balls, and goals
        white_balls = []
        orange_balls = []
        goals = []
        print("example enpoiint before" + str(self.end_points[0]))
        for obj in self.end_points:
            obj_center = obj['center']
            obj_type = obj['type']
            print("when sorting, sorting object of type: " + obj_type + " with center: " + str(obj_center))
            # Calculate distance from the current position to the object considering walls
            distance = self.taxi_distance(current_position, obj_center)

            # Check the color of the object
            if obj_type == "white-ball":
                white_balls.append(obj)
            elif obj_type == "orange-ball":
                orange_balls.append(obj)
            elif obj_type == "goal":
                goals.append(obj)

        # Sort white balls by distance
        white_balls.sort(key = lambda x: self.taxi_distance(current_position, x['center']))
        # Sort orange balls by distance

        # Combine the sorted lists
        sorted_end_points = white_balls + orange_balls + goals
        print("example endpoint after" + str(sorted_end_points[0]))
        self.end_points = sorted_end_points

    def taxi_distance(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def get_center_coords(self, obj):
        center_x = (obj['x_min'] + obj['x_max']) // 2
        center_y = (obj['y_min'] + obj['y_max']) // 2
        return center_x, center_y

    def scaled_to(self, new_width, new_height):
        new_grid = Grid(new_width, new_height)
        block_width = self.width // new_width
        block_height = self.height // new_height

        new_end_points = []
        for point in self.end_points:
            new_point = {
                'center': (point['center'][0] // block_width, point['center'][1] // block_height),
                'type': point['type']
            }
            new_end_points.append(new_point)

        new_grid.end_points = new_end_points

        for new_y in range(new_height):
            for new_x in range(new_width):
                start_y = int(new_y * block_height)
                end_y = min(int((new_y + 1) * block_height), self.height)
                start_x = int(new_x * block_width)
                end_x = min(int((new_x + 1) * block_width), self.width)

                found_non_empty = False
                for orig_y in range(start_y, end_y):
                    if found_non_empty:
                        break
                    for orig_x in range(start_x, end_x):
                        current_cell = self.grid[orig_y][orig_x]
                        if current_cell != 0:
                            new_grid.grid[new_y][new_x] = current_cell
                            found_non_empty = True
                            break

        return new_grid

    def cell_withing_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def __getitem__(self, item):
        x, y = item
        return self.grid[y][x]

    def __setitem__(self, key, value):
        x, y = key
        self.grid[y][x] = value

    def __str__(self):
        return "\n".join([" ".join([str(element) for element in row]) for row in self.grid])
