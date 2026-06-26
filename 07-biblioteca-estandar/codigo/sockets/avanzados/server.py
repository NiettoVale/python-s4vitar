#!/usr/bin/env python3

import socket

from clases import ClientThread

HOST = "127.0.0.1"
PORT = 4444


def start_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))

        print("[+] Esperando conexiones entrantes...\n")

        while True:
            server.listen()
            connection, address = server.accept()
            new_thread = ClientThread(connection, address)
            new_thread.start()


if __name__ == "__main__":
    start_socket()
