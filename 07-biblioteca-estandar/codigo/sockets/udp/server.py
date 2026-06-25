#!/usr/bin/env python3

import socket

# Definimos el host y el puerto
HOST = '127.0.0.1'
PORT = 4444

def start_udp_server():
    # Creamos el socket del servidor
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        # Vinculamos el socket a esa direccion y puerto
        server.bind((HOST, PORT))
        print(f'\n[+] El servidor UDP esta en escucha en ({HOST}, {PORT}).\n')
        
        while True:
            data, address = server.recvfrom(1024)
            print(f'Mensaje enviado por el cliente: {data.decode('utf-8')}')
            print(f'[+] Informacion del cliente que nos ha enviado el mensaje: {address}')
    
start_udp_server()
