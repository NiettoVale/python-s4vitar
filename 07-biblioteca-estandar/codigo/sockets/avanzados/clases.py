#!/usr/bin/env python3

import threading


class ClientThread(threading.Thread):
    def __init__(self, client, address):
        super().__init__()
        self.client = client
        self.address = address

        print(f"\n[+] Nuevo cliente conectado: {self.address[0]}:{self.address[1]}")

    def run(self):
        message = ""

        while True:
            data = self.client.recv(1024)
            message = data.decode("utf-8")
            server_message = f"\n[+] Mensaje recibido: {message}".encode("utf-8")
            if message.lower().strip() == "bye":
                break

            print(f"\n[+] Mensaje enviado por el cliente: {message}")
            self.client.send(server_message)
        print(
            f"\n[!] El cliente ({self.address[0]}:{self.address[1]}) se ha desconectado..."
        )

        self.client.close()
