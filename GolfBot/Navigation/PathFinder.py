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

            for neighbor in self.get_neighbors(current, 2):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    print("came from" + str(current))
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

    def get_neighbors(self, node, robot_size=10):
        neighbors = []
        current_x, current_y = node

        movements = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (1, 1), (-1, -1), (1, -1), (-1, 1),
                     ]

        for dx, dy in movements:
            neighbor_x = current_x + dx
            neighbor_y = current_y + dy
            if self.is_valid_position(neighbor_x, neighbor_y, robot_size):
                print('Neighbors: ' + str(neighbor_x), str(neighbor_y))
                neighbors.append((neighbor_x, neighbor_y))

        return neighbors

    def is_valid_position(self, x, y, robot_size):
        within = self.grid.cell_withing_bounds(x, y)
        if not within:
            return False
        if self.grid[x, y] == 1:
            return False
        #if robot_will_colide(x, y, robot_size):
        #return False
        return True

    def find_path(self, start, goal):
        full_path = self.astar(start, goal)
        #corner_path = self.identify_corners(full_path)
        #final_path = corner_path.append(goal)
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
        return self.water_search(current_position, 7, 100)

    def find_nearest_goal(self, current_position):
        print('searching for a goal')
        return self.water_search(current_position, 8, 100)

    def water_search(self, current_position, search_type, radius=5):
        current_x, current_y = current_position
        grid = self.grid
        # Generate movement based on radius
        movement = [(dx, dy) for dx in range(-radius, radius + 1) for dy in range(-radius, radius + 1) if
                    (dx, dy) != (0, 0)]
        for dx, dy in movement:
            neighbor_x = current_x + dx
            neighbor_y = current_y + dy
            # Check if the neighbor is within the grid
            if grid.cell_withing_bounds(neighbor_x, neighbor_y):
                if self.grid[neighbor_x, neighbor_y] == search_type:
                    return neighbor_x, neighbor_y
        return None

    def taxi_distance(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
