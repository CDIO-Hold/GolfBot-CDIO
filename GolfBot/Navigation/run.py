from Grid import Grid
from PathFinder import PathFinder

if __name__ == "__main__":

    grid = Grid(width=128, height=72)
    # Example detected objects with bounding box coordinates
    x1 = 0  # Starting x-coordinate of the bounding box (left edge)
    y1 = 100  # Starting y-coordinate of the bounding box (top edge)
    x2 = 270# Ending x-coordinate of the bounding box (just a small width)
    y2 = 400  # Ending y-coordinate of the bounding box (full height of the screen)

    detected_objects = [
        {'xmin': x1, 'ymin': y1, 'xmax': x2, 'ymax': y2, 'type': 'wall'},
        #{'xmin': 300, 'ymin': 200, 'xmax': 350, 'ymax': 250, 'type': 'wall'},
        #{'xmin': 250, 'ymin': 550, 'xmax': 300, 'ymax': 600, 'type': 'ball'}
    ]

    grid.add_detected_object(detected_objects)
    grid.display_grid()
    # Example usage
    start_position = (0, 0)
    goal_position = (50, 20)
    pathfinder = PathFinder(grid)
    path = pathfinder.astar(start_position, goal_position)
    print("Path:", path)


    # Function to visualize the path on the grid
    def visualize_path(grid, path, start, goal):
        grid_display = grid.grid.copy()
        for pos in path:
            grid_display[pos] = 2
        grid_display[start] = 6
        grid_display[goal] = 9
        for row in grid_display:
            print(' '.join(str(int(cell)) for cell in row))

    visualize_path(grid, path, start_position, goal_position)
#Path: [
# (0, 0),(1, 0),(1, 1),(1, 2),(1, 3),
# (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
# (1, 9), (2, 9), (3, 9), (4, 9), (5, 9),
# (6, 9), (7, 9), (8, 9), (9, 9)]


#driver = Driver(tank, speed, wheel, Circle(0))

#for pos in path:
 #   target_position = Position(pos[0], pos[1])
  #  driver.drive_to(target_position)

