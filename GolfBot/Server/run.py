from GolfBot.Server.Connector import Connector
from YOLO import Yolo
from GolfBot.Server.Navigation.Grid import Grid

if __name__ == "__main__":
    yolo = Yolo()
    grid = Grid(1280, 720)
    conn = Connector(yolo, grid, capture_interval=30)
    conn.run()

    '''
    image_grid = Grid(10, 10)
    # Example detected objects with bounding box coordinates
    x1 = 5  # Starting x-coordinate of the bounding box (left edge)
    y1 = 0  # Starting y-coordinate of the bounding box (top edge)
    x2 = 9 # Ending x-coordinate of the bounding box (just a small width)
    y2 = 0  # Ending y-coordinate of the bounding box (full height of the screen
    detected_objects = [
        {'xmin': x1, 'ymin': y1, 'xmax': x2, 'ymax': y2, 'type': 'wall'},
        {'xmin': 0, 'ymin': 4, 'xmax': 5, 'ymax': 4, 'type': 'wall'},
        #{'xmin': 250, 'ymin': 550, 'xmax': 300, 'ymax': 600, 'type': 'ball'}
    ]
    image_grid.add_detected_object(detected_objects)
    image_start_position = (2, 7)
    image_ball2_position = (3, 2)
    image_ball_position = (7, 1)
    image_grid.add_object(image_start_position[0], image_start_position[1], 6)
    #image_grid.add_object(image_end_position[0], image_end_position[1], 9)

    image_grid.add_object(image_ball_position[0],image_ball_position[1],7)
    image_grid.add_object(image_ball2_position[0],image_ball2_position[1],7)
    print("Image grid:")
    print(image_grid)
    print("\n")

    robot_grid = image_grid.scaled_to(10, 10)
    print("Robot grid:")
    print(robot_grid)
    # create path
    pathfinder = PathFinder(robot_grid)

    def scale_position(position, original_grid, scaled_grid):
        x, y = position
        new_x = int(x / original_grid.width * scaled_grid.width)
        new_y = int(y / original_grid.height * scaled_grid.height)
        return new_x, new_y
    robot_start_position = scale_position(image_start_position, image_grid, robot_grid)
    #robot_end_position = scale_position(image_end_position, image_grid, robot_grid)
    robot_end_position = pathfinder.find_nearest_ball(robot_start_position)
    print("Robot end position:", robot_end_position)
    path = pathfinder.astar(robot_start_position, robot_end_position)
    print("Path:", path)

    # Function to visualize the path on the grid
    def visualize_path(grid, path, start, goal):
        display_grid = Grid(grid.width, grid.height)
        display_grid.grid = grid.grid.copy()
        for pos in path:
            display_grid.add_object(pos[0], pos[1], 2)
        display_grid.add_object(start[0], start[1], 6)
        display_grid.add_object(goal[0], goal[1], 9)
        print(display_grid)

    visualize_path(robot_grid, path, robot_start_position, robot_end_position)
    '''

