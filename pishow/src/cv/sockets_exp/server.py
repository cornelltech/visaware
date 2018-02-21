#!/usr/bin/env python
"""server.py - simple socket server experiment"""

import socket


SOCKET_PORT = 5005
MAX_QUEUED_CONNECTIONS = 5


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind((socket.gethostname(), SOCKET_PORT))
    server_socket.bind(("", SOCKET_PORT))
    server_socket.listen(MAX_QUEUED_CONNECTIONS)
    while True:
        # accept connections from outside
        (client_socket, address) = server_socket.accept()
        # now do something with client_socket
        data = client_socket.recv(1)
        print data
