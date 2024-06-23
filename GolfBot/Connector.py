from socket import socket, AF_INET, SOCK_DGRAM
from Navigation import Grid
from Navigation.PathFinder import PathFinder
from YOLO import Yolo
import time


class Connector:
    def __init__(self, yolo: Yolo, grid: Grid, host='127.0.0.1', port=8000, capture_interval=30):
        self.yolo = yolo
        self.grid = grid
        self.host = host
        self.port = port
        self.capture_interval = capture_interval

    def run(self):
        while True:
            start_time = time.time()
            print('Before')
            img, detected_objects = self.yolo.run()
            print('After')
            if img is not None and detected_objects is not None:
                self.process_image(detected_objects)

            elapsed_time = time.time() - start_time
            sleep_time = self.capture_interval - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    def process_image(self, detected_objects):
        self.grid.add_detected_object(detected_objects)
        #self.grid.add_detected_endpoint(detected_objects)
        self.grid = self.grid.scaled_to(128, 72)

        print(self.grid)
        pathfinder = PathFinder(self.grid)

        has_white_ball = any(obj['type'] == 'white-ball' for obj in detected_objects)
        has_goal = any(obj['type'] == 'goal' for obj in detected_objects)
        has_robot = any(obj['type'] == 'robot' for obj in detected_objects)

        robot_position = None
        for obj in detected_objects:
            if obj['type'] == 'robot':
                robot_position = self.grid.get_center_coords(obj)
                break

        if has_robot and robot_position:
            print(f"Robot detected at: {robot_position}")
            self.send_data(robot_position, 'update_robot_pos')
        else:
            robot_position = (3, 3)

        end_position = None
        if len(self.grid.end_points) > 0: #should be 0
            self.grid.sorted_end_points(robot_position)
            end_position = self.grid.end_points[1]['center'] #should be 0
            print('Found the position:', end_position)
            path = pathfinder.find_path(robot_position, end_position)
            print(self.grid.end_points)
            print(path)
            self.visualize_path(path, robot_position, end_position)
            self.send_data(path, 'goto')
        else:
            print('no endpoints')

    def visualize_path(self, path, start, goal):
        display_grid = self.grid
        for pos in path:
            display_grid.add_object(pos[0], pos[1], 2)
        display_grid.add_object(start[0], start[1], 6)
        display_grid.add_object(goal[0], goal[1], 9)
        print(display_grid)

    def send_data(self, path, action):
        try:
            if not path:
                print("No path to send.")
                return

            last_position = path[-1]  # Get the last coordinates in the path
            data = f"{action} {last_position[0]},{last_position[1]}"

            client_socket = socket(AF_INET, SOCK_DGRAM)
            client_socket.sendto(data.encode(), (self.host, self.port))
            response, _ = client_socket.recvfrom(1024)
            print(f"Response from server: {response.decode()}")
            client_socket.close()
        except Exception as e:
            print(f"Error communicating with the old environment: {e}")
