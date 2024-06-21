from socket import socket, AF_INET, SOCK_DGRAM

localhost = "127.0.0.1"
port = 8000
sock = socket(AF_INET, SOCK_DGRAM)
sock.connect((localhost, port))

print("Sending")
while True:
    message = input()
    payload = message.encode("utf-8")
    sock.send(payload)
    if message == "exit":
        break

    answer = sock.recv(1024).decode("utf-8")

    print("[SERVER]: {}".format(answer))