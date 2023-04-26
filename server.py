import socket

# the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind to the recieving socket, port
address = (socket.gethostname(), 1600)
s.bind((address))
#listen for signal
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address}")
    clientsocket.send(bytes("Welcome in.","utf-8"))

    clientsocket.close()

