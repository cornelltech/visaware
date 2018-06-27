#!/usr/bin/env python3

import socket

HOST = '128.84.84.150'
PORT = 5050

def main(sock):
    sock.sendto(b'x', (HOST, PORT))

if __name__ == "__main__":
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    main(SOCK)
