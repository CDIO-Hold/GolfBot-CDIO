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

    def get_neighbors(self, node):
        neighbors = []
        current_x, current_y = node

        # Define the relative movements for neighbors (left, right, up, down)
        movements = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (-2, 0), (2, 0), (0, -2), (0, 2),
                     (-3, 0), (3, 0), (0, -3), (0, 3),
                     (-4, 0), (4, 0), (0, -4), (0, 4),
                     (-5, 0), (5, 0), (0, -5), (0, 5),
                     ]

        for dx, dy in movements:
            neighbor_x = current_x + dx
            neighbor_y = current_y + dy

            # Check if the neighbor is within bounds and is not a wall
            if (0 <= neighbor_x < self.grid.width and
                    0 <= neighbor_y < self.grid.height and
                    self.grid.grid[neighbor_x][neighbor_y] == 0):
                neighbors.append((neighbor_x, neighbor_y))
        return neighbors




