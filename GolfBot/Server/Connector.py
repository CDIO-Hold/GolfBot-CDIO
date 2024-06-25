from socket import socket, AF_INET, SOCK_DGRAM

import cv2

from GolfBot.Server.Navigation import Grid
from GolfBot.Server.Navigation.PathFinder import PathFinder
from YOLO import Yolo
import time


class Connector:
    def __init__(self, yolo: Yolo, grid: Grid, host='127.0.0.1', port=8000, capture_interval=30):
        self.yolo = yolo
        self.grid = grid
        self.capture_interval = capture_interval
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def run(self):
        self.socket.connect((self.host, self.port))
        while True:
            start_time = time.time()
            print('Before')
            img, detected_objects = self.yolo.find_objects()
            print('After')
            if img is not None and detected_objects is not None:
                cv2.imwrite("../Current.png", img)
                self.process_image(detected_objects)

            elapsed_time = time.time() - start_time
            sleep_time = self.capture_interval - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    def process_image(self, detected_objects):
        for obj in detected_objects:
            self.grid.add_box(obj)

        self.grid = self.grid.scaled_to(128, 72)

        #print(self.grid)
        pathfinder = PathFinder(self.grid)

        has_robot = any(obj['type'] == 'robot' for obj in detected_objects)

        robot_position = None
        for obj in detected_objects:
            if obj['type'] == 'robot':
                robot_position = self.grid.get_center_coords(obj)

        if has_robot and robot_position:
            print(f"Robot detected at: {robot_position}")
            x, y = robot_position
            self.send(f"update_robot_pos {x},{y}")
            # self.send_data(robot_position, 'update_robot_pos')
        else:
            robot_position = (0, 0)

        if len(self.grid.end_points) > 0:
            self.grid.sorted_end_points(robot_position)
            end_position = self.grid.end_points[0]['center']
            print('Found the position:', end_position)
            path = pathfinder.find_path(robot_position, end_position)
            print("Path:", path)
            #self.send_path(path)
        else:
            print('no endpoints')

    def visualize_path(self, path, start, goal):
        display_grid = self.grid
        for pos in path:
            display_grid.add_object(pos[0], pos[1], 2)
        display_grid.add_object(start[0], start[1], 6)
        display_grid.add_object(goal[0], goal[1], 9)
        print(display_grid)

    def send(self, message: str):
        data = message.encode("utf-8")
        print(f"Sending: '{message}'")
        self.socket.send(data)
        response = self.socket.recv(1024)
        print(f"Response from server '{response.decode()}'")

    def send_path(self, path: list):
        for position in path:
            x, y = position
            self.send(f"goto {x},{y}")

    def send_data(self, path, action):
        try:
            if not path:
                print("No path to send.")
                return

            if 'goto' in action:
                for position in path:
                    data = f"goto {position[0]},{position[1]}"
                    self.socket.send(data.encode())
                    response, _ = self.socket.recvfrom(1024)
                    print(f"Response from server: {response.decode()}")
            elif 'update_robot_pos' in action:
                data = f'{action} {path[0]},{path[1]}'
                self.socket.send(data.encode())
                response, _ = self.socket.recvfrom(1024)
                print(f"Response from server: {response.decode()}")

        except Exception as e:
            print(f"Error communicating with the old environment: {e}")

    """ # Testing if it even works with goto
    def send_input_data(self):
        while True:
            action = input("command")
            if action == "exit":
                break

            if action.startswith("goto"):
                client_socket = socket(AF_INET, SOCK_DGRAM)
                client_socket.connect((self.host, self.port))
                x, y = action.split(" ")[1].split(",")
                data = f'goto {x},{y}'
                client_socket.sendto(data.encode(), (self.host, self.port))
                response, _ = client_socket.recvfrom(1024)
                print(f"Response from server: {response.decode()}")
                client_socket.close()
    """