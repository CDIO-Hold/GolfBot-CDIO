from socket import socket, AF_INET, SOCK_DGRAM

localhost = "127.0.0.1"
port = 8000
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((localhost, port))

position = (0, 0)

print("Listening")
while True:
    data, sender = sock.recvfrom(1024)
    command = data.decode("utf-8")

    answer = b'Accepted'
    if command == "exit":
        break
    elif command.startswith("goto"):
        target = command.split(" ")[1]
        x, y = target.split(",")
        target = int(x), int(y)
        print(f"Moving robot to {target}")
        position = target
    elif command == "info":
        print(f"Position: {position}")
    else:
        answer = b'Unknown command'

    sock.sendto(answer, sender)

print("Shutting down server")
sock.close()