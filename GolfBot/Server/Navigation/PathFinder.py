import heapq


class PathFinder:
    def __init__(self, grid):
        self.grid = grid

    def astar(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.taxi_distance(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                print("Goal reached!")
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.taxi_distance(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        print("No path found")
        return []

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def get_neighbors(self, node):
        neighbors = []
        current_x, current_y = node

        movements = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (1, 1), (-1, -1), (1, -1), (-1, 1),
                     ]

        for dx, dy in movements:
            neighbor_x = current_x + dx
            neighbor_y = current_y + dy
            if self.is_valid_position(neighbor_x, neighbor_y):
                if not self.will_collide(neighbor_x, neighbor_y, 50):
                    neighbors.append((neighbor_x, neighbor_y))

        return neighbors

    def is_valid_position(self, x, y):
        within = self.grid.cell_withing_bounds(x, y)
        if not within:
            return False
        if self.grid[x, y] == 1:
            return False
        return True

    def will_collide(self, neighbor_x, neighbor_y, robot_size):
        collision = False
        for i in range(0, robot_size):
            for j in range(0, robot_size):
                if not self.is_valid_position(neighbor_x + i, neighbor_y + j):
                    #print("will collide at: ", neighbor_x + i, neighbor_y + j)
                    collision = True
                if not self.is_valid_position(neighbor_x + i, neighbor_y - j):
                    #print("will collide at: ", neighbor_x + i, neighbor_y - j)
                    collision = True
                if not self.is_valid_position(neighbor_x - i, neighbor_y + j):
                    #print("will collide at: ", neighbor_x - i, neighbor_y + j)
                    collision = True
                if not self.is_valid_position(neighbor_x - i, neighbor_y - j):
                    #print("will collide at: ", neighbor_x - i, neighbor_y - j)
                    collision = True
        return collision

    def find_path(self, start, end_position):
        staggered = end_position['staggered']
        end_goal = end_position['center']
        if staggered is None: #go straight to end goal
            full_path = self.astar(start, end_goal)
        else: #first go to staggered position then end goal
            full_path = self.astar(start, staggered)
        #    print('path to staggered: ', full_path)
         #   print('path to goal from: ', full_path)
        print('path before' + str(full_path))
        full_path = self.identify_corners(full_path)
        #final_path = corner_path.append(goal)
        full_path.append(end_goal)
        return full_path

    def identify_corners(self, path):
        corners = []
        for i in range(1, len(path) - 1):
            prev = path[i - 1]
            current = path[i]
            next = path[i + 1]

            # Calculate direction of movement
            dx1, dy1 = current[0] - prev[0], current[1] - prev[1]
            dx2, dy2 = next[0] - current[0], next[1] - current[1]

            # Check for change in direction
            if (dx1 != dx2) or (dy1 != dy2):
                corners.append(current)

        return corners

    def find_nearest_ball(self, current_position):
        print('searching for a ball')

    def find_nearest_goal(self, current_position):
        print('searching for a goal')

    def taxi_distance(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
