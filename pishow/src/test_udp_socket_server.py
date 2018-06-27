#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 5050

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    while True:
        data, addr = sock.recvfrom(1)
        print('received data: ', data)

if __name__ == "__main__":
    main()
