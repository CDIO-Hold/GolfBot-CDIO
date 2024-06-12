import socket

# from Shared.Position import Position
# from YOLO import Yolo

# Define the server address and port
HOST = "192.168.124.44"  # Listen on all available interfaces
PORT = 10002             # Port to listen on

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")

# Accept a connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

conn.sendall(b'start')

exit(0)

yolo = Yolo()

path = [Position(1000, 0), Position(500, 300), Position(-200, 200), Position(0, 0)]
try:
    while True:
        # Receive data from the client
        data = conn.recv(1024)
        if not data:
            break
        command = data.decode()
        print(f"SERVER: Received {command}")

        # Execute command
        if command == "TEST":
            print("Test indeed")
        elif command == 'detect':
            yolo.run()


        for point in path:
                driver.drive_to(point)


        # Send data back to the client
        conn.sendall(b'Command executed')
        conn.sendall(b'Initialize')

finally:
    # Close the connection
    conn.close()
    server_socket.close()