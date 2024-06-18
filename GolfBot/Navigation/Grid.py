import numpy as np

class Grid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height))

    def add_detected_object(self, detected_objects):
        for obj in detected_objects:
            obj_type = obj['type']
            if obj_type == "ball":
                print("adding ball")
                center_x = (obj['xmin'] + obj['xmax']) / 2
                center_y = (obj['ymin'] + obj['ymax']) / 2
                grid_x, grid_y = self.map_point_to_grid(center_x, center_y)
                self.grid[grid_y, grid_x] = 7
            else:
                xmin = obj['xmin']
                xmax = obj['xmax']
                ymin = obj['ymin']
                ymax = obj['ymax']

                # Iterate over the bounding box coordinates to fill the grid
                for x in range(xmin, xmax + 1):
                    for y in range(ymin, ymax + 1):
                        grid_x, grid_y = self.map_point_to_grid(x, y)
                        self.grid[grid_y, grid_x] = 1
    def add_test_object(self, x,y):
        self.grid[y,x] = 1

    def map_point_to_grid(self, x, y, img_width=1280, img_height=720):
        #map
        grid_x = int(x / img_width * self.width)
        grid_y = int(y / img_height * self.height)
        return grid_x, grid_y





    def display_grid(self):
        for row in self.grid:
            print(' '.join(str(int(cell)) for cell in row))
