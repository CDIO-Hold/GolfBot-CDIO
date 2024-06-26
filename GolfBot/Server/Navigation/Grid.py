import numpy as np
from queue import Queue


class Grid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.end_points = []

    def add_box(self, box, object_type: str):
        #print(f"Adding {object_type}")
        number = self.obj_type_to_int(object_type)
        self.add_2d_object(int(box.x1), int(box.x2), int(box.y1), int(box.y2), number)
        return

    def add_endpoint(self, center, endpoint_type: str, safe_zone=0):
            center_x, center_y = (int (n) for n in center.as_tuple())
            self.add_object(center_x, center_y, self.obj_type_to_int(endpoint_type))

            # if that endpoint has something close to it, create a staggered endpoint
            distance_and_direction = self.direction_and_distance_to_closest_object(center_x, center_y, safe_zone)
            direction = next(iter(distance_and_direction))
            distance = distance_and_direction[direction]
            if distance > safe_zone:
                end_point = {
                    'center': (center_x, center_y),
                    'staggered': None,
                    'type': endpoint_type
                }
                self.add_end_point(end_point)
            else:
                #print("creating staggered endpoint bases on the direction and distance to closest object")
                stagger_distance = safe_zone - distance
                #staggered_end_point = self.stagger_end_point(center_x, center_y, endpoint_type, direction, stagger_distance)
                #self.add_end_point(staggered_end_point)
            return

    #function that determines if something is close to a recently added endpoint
    def direction_and_distance_to_closest_object(self, center_x, center_y, safe_zone_radius):
        #movements in all directions based on safe_zone_radius
        straight_up_movement = [(0, i) for i in range(1, safe_zone_radius + 1)]
        straight_down_movement = [(0, -i) for i in range(1, safe_zone_radius + 1)]
        straight_left_movement = [(-i, 0) for i in range(1, safe_zone_radius + 1)]
        straight_right_movement = [(i, 0) for i in range(1, safe_zone_radius + 1)]
        #diagonal_up_right = [(i, i) for i in range(1, safe_zone_radius + 1)]
        #diagonal_up_left = [(-i, i) for i in range(1, safe_zone_radius + 1)]
        #diagonal_down_right = [(i, -i) for i in range(1, safe_zone_radius + 1)]

        straight_up = {"straight_up": safe_zone_radius + 1}
        straight_down = {"straight_down": safe_zone_radius + 1}
        straight_left = {"straight_left": safe_zone_radius + 1}
        straight_right = {"straight_right": safe_zone_radius + 1}
        #diagonal_up_right_distance = 0
        #diagonal_up_left_distance = 0
        #diagonal_down_right_distance = 0

        # loop through all movements and add the length of the movement to the distance if there is an object in the way
        for movement in straight_up_movement:
            current_distance = abs(movement[1])
            current_cell = (center_x, center_y - movement[1])
            #print("checking straight up cell on grid: " + str(current_cell))
            if not self.is_empty_space(current_cell[0], current_cell[1]):
                #print('found an obstacle above ' + str(current_distance) + ' away')
                straight_up['straight_up'] = current_distance
                break


        for movement in straight_down_movement:
            current_distance = abs(movement[1])
            #print("current distance: " + str(current_distance))
            current_cell = (center_x, int(center_y - movement[1])) # should maybe be current_cell = (center_x, center_y + movement[1])
            #print("checking straight down cell on grid: " + str(current_cell))
            if not self.is_empty_space(current_cell[0], current_cell[1]):
                straight_down['straight_down'] = current_distance
                break

        for movement in straight_left_movement:
            current_distance = abs(movement[0])
            current_cell = (center_x + movement[0], center_y)
            #print("checking straight left cell on grid: " + str(current_cell))
            if not self.is_empty_space(current_cell[0], current_cell[1]):
                #print('found an obstacle to the left ' + str(current_distance) + ' away')
                straight_left['straight_left'] = current_distance
                break

        for movement in straight_right_movement:
            current_distance = abs(movement[0])
            current_cell = (center_x + movement[0], center_y)
            #print("checking straight right cell on grid: " + str(current_cell))
            if not self.is_empty_space(current_cell[0], current_cell[1]):
                #print('found an obstacle to the right ' + str(current_distance) + ' away')
                straight_right['straight_right'] = current_distance
                break

        #find the direction with the closest distance
        dict_list = [straight_up, straight_down, straight_left, straight_right]
        #print('before sorting: ' + str(dict_list))
        sorted_dicts = sorted(dict_list, key=lambda x: next(iter(x.values())))
        #print('after sorting: ' + str(sorted_dicts))
        min_dict = sorted_dicts[0]
        return min_dict

    def stagger_end_point(self, center_x, center_y, type, direction, distance):
        staggered_center_y = 2
        staggered_center_x = 2
        if direction == "straight_up":
            staggered_center_y = center_y + distance
            staggered_center_x = center_x
        elif direction == "straight_down":
            staggered_center_y = center_y - distance
            staggered_center_x = center_x
        elif direction == "straight_left":
            staggered_center_x = center_x + distance
            staggered_center_y = center_y
        elif direction == "straight_right":
            staggered_center_x = center_x - distance
            staggered_center_y = center_y

        return {
                'center': (center_x, center_y),
                'staggered': (staggered_center_x, staggered_center_y),
                'type': type
                }


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
        self.end_points.append(end_point)
        return

    def sorted_end_points(self, current_position):
        # Initialize lists to store white balls, orange balls, and goals
        white_balls = []
        orange_balls = []
        goals = []
        for obj in self.end_points:
            obj_type = obj['type']
            # Check the color of the object
            if obj_type == "white-ball":
                white_balls.append(obj)
            elif obj_type == "orange-ball":
                orange_balls.append(obj)
            elif obj_type == "goal":
                goals.append(obj)

        # Sort white balls by distance
        # Update the sorting logic
        white_balls.sort(key=lambda x: (
        self.taxi_distance(current_position, x['center']) <= 60, self.taxi_distance(current_position, x['center'])))

        # Sort orange balls by distance

        # Combine the sorted lists
        sorted_end_points = white_balls + orange_balls + goals
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

       #scale points and staggered points using def scale_points
        new_grid.end_points = self.scaled_points(block_width, block_height)
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

    def scaled_points(self, block_width, block_height):
        scaled_points = []
        for point in self.end_points:
            if point['staggered'] is None:
                scaled_point = {
                    'center': (point['center'][0] // block_width, point['center'][1] // block_height),
                    'staggered': None,
                    'type': point['type']
                }
                scaled_points.append(scaled_point)
            else:
                scaled_point = {
                'center': (point['center'][0] // block_width, point['center'][1] // block_height),
                'staggered': (point['staggered'][0] // block_width, point['staggered'][1] // block_height),
                'type': point['type']
                }
                scaled_points.append(scaled_point)
        return scaled_points
    def cell_withing_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_empty_space(self, x, y):
        within = self.cell_withing_bounds(x, y)
        if not within:
            return False
        #print("checking if empty space at: " + str(x) + ", " + str(y) + " with value: " + str(self.grid[y][x]))
        if self.grid[y][x] == 1:
            return False
        return True
    def obj_type_to_int(self, obj_type):
        if obj_type == "wall":
            return 1
        elif obj_type == "white-ball":
            return 2
        elif obj_type == "orange-ball":
            return 3
        elif obj_type == "robot":
            return 4
        elif obj_type == "goal":
            return 8
        elif obj_type == "cross":
            return 1
        elif obj_type == "egg":
            return 1
        else:
            return 0


    def __getitem__(self, item):
        x, y = item
        return self.grid[y][x]

    def __setitem__(self, key, value):
        x, y = key
        self.grid[y][x] = value

    def __str__(self):
        return "\n".join([" ".join([str(element) for element in row]) for row in self.grid])
