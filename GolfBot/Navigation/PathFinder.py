import heapq


class PathFinder:
    def __init__(self, grid):
        self.grid = grid

    def taxi_distance(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def astar(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.taxi_distance(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.taxi_distance(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def get_neighbors(self, node, robot_size=2):
        neighbors = []
        current_x, current_y = node

        # Define the relative movements for neighbors in a larger range
        movements = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     #(-2, 0), (2, 0), (0, -2), (0, 2),
                     #(-3, 0), (3, 0), (0, -3), (0, 3),
                     #(-4, 0), (4, 0), (0, -4), (0, 4),
                     #(-5, 0), (5, 0), (0, -5), (0, 5)
                     ]

        for dx, dy in movements:
            neighbor_x = current_x + dx
            neighbor_y = current_y + dy

            if self.is_valid_position(neighbor_x, neighbor_y, robot_size):
                neighbors.append((neighbor_x, neighbor_y))

        return neighbors

    def is_valid_position(self, x, y, robot_size):
        # Check the area around (x, y) for obstacles
        half_size = (int(robot_size / 2)) # the double slash is used to get the integer division
        for i in range(x - half_size, x + half_size + 1):
            for j in range(y - half_size, y + half_size + 1):
                if not (0 <= i < self.grid.width and 0 <= j < self.grid.height):
                    return False  # Out of bounds
                if self.grid.grid[i][j] != 0:
                    return False  # Obstacle detected
        return True




