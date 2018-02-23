#!/usr/bin/env python
"""server.py - simple socket server experiment"""

import socket


SOCKET_PORT = 5005

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if socket.gethostname() == "pishow-150":
        server_hostname = "pishow-130"
    elif socket.gethostname() == "pishow-130":
        server_hostname = "pishow-150"

    print "connecting to server %s" % server_hostname
    client_socket.connect((server_hostname, SOCKET_PORT))
    client_socket.send('b')
    client_socket.close()
