import numpy as np


class Grid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

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
            elif obj_type == "orange-ball":
                print("adding orange-ball")
                center_x, center_y = self.get_center_coords(obj)
                self.add_object(center_x, center_y, 3)
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
                    self.grid[j][i] = obj_type

    def get_center_coords(self, obj):
        center_x = (obj['x_min'] + obj['x_max']) // 2
        center_y = (obj['y_min'] + obj['y_max']) // 2
        return center_x, center_y

    def scaled_to(self, new_width, new_height):
        new_grid = Grid(new_width, new_height)
        block_width = self.width / new_width
        block_height = self.height / new_height

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
