import numpy as np


class Grid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def add_detected_object(self, detected_objects):
        for obj in detected_objects:
            obj_type = obj['type']
            if obj_type == "ball":
                print("adding ball")
                center_x, center_y = self.get_center_coords(obj)
                self.add_object(center_x, center_y, 7)
            if obj_type == "goal":
                print("adding goal")
                center_x, center_y = self.get_center_coords(obj)
                self.add_object(center_x, center_y, 8)
            if obj_type == "robot":
                print("adding robot")
                center_x, center_y = self.get_center_coords(obj)
                self.add_object(center_x, center_y, 9)
            if obj_type == "wall":
                print("adding wall")
                xmin = obj['x_min']
                xmax = obj['x_max']
                ymin = obj['y_min']
                ymax = obj['y_max']
                # Iterate over the bounding box coordinates to fill the grid
                self.add_2d_object(xmin, xmax, ymin, ymax, 1)

    def add_object(self, x, y, obj_type):
        x = int(x)
        y = int(y)
        self.grid[y][x] = obj_type

    def add_2d_object(self, xmin, xmax, ymin, ymax, obj_type):
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                #print("i: " + str(i) + "j: " + str(j))
                self.grid[j][i] = obj_type

    def get_center_coords(self, obj):
        center_x = (obj['x_min'] + obj['x_max']) / 2
        center_y = (obj['y_min'] + obj['y_max']) / 2
        return center_x, center_y

    def scaled_to(self, new_width, new_height):
        new_grid = Grid(new_width, new_height)
        block_width = self.width // new_width
        block_height = self.height // new_height

        for new_y in range(new_height):
            for new_x in range(new_width):
                # Determine the range of original grid cells that map to the new grid cell
                start_y = int(new_y * block_height)
                end_y = min(int((new_y) * block_height), self.height)
                start_x = int(new_x * block_width)
                end_x = min(int((new_x) * block_width), self.width)

                # Check if any cell in the corresponding block contains a non-empty value
                for orig_y in range(start_y, end_y):
                    for orig_x in range(start_x, end_x):
                        if self.grid[orig_y][orig_x] != 0:
                            new_grid.grid[new_y][new_x] = self.grid[orig_y][orig_x]
                            break
                    if new_grid[new_y, new_x] != 0:
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