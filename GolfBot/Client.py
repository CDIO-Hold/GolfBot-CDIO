# EV3 is the client
from socket import socket
from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from Robot import Driver, Collector, Robot
from Shared import Position, Angle, degrees

HOST = '0.0.0.0'  # The IP address of your laptop
PORT = 10002             # The same port as used by the server

# Create a socket
print("Creating a socket")
client_socket = socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
print("Connecting to the server")
client_socket.connect((HOST, PORT))

# Send data to the server
client_socket.sendall(b'TEST')


# Receive data from the server
data = client_socket.recv(1024)
message = data.decode('utf-8')
print("CLIENT: Received {message}")

if message == 'start':
    # Initialize EV3 Brick and motors
    ev3 = EV3Brick()

    left_wheel = Motor(Port.B)
    right_wheel = Motor(Port.C)
    driver = Driver(left_wheel, right_wheel)

    left_motor = Motor(Port.A)
    right_motor = Motor(Port.D)
    collector = Collector(left_motor, right_motor, 800)

    robot = Robot(driver, collector, Position(0, 0), 10, Angle(0, degrees))
elif message == 'Drive':
    print("Drive")

# Close the connection
client_socket.close()