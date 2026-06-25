#!/usr/bin/env python3

import socket

# Dirección y puerto en los que el servidor escuchará conexiones entrantes.
# '' o '0.0.0.0' como host significa "escuchar en todas las interfaces disponibles".
# '127.0.0.1' limita la escucha solo a la interfaz loopback (solo conexiones locales).
HOST = '127.0.0.1'
PORT = 4444


def start_server_v1():
    """
    Versión tradicional: los sockets se cierran manualmente.
    Problema: si se lanza una excepción antes de los close(),
    ambos sockets (servidor y conexión) quedan sin cerrar.
    """
    # AF_INET     → IPv4
    # SOCK_STREAM → TCP (orientado a conexión, fiable y ordenado)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind() asocia el socket a una dirección y puerto específicos.
    # Es el paso que "reserva" el puerto en el sistema operativo.
    server.bind((HOST, PORT))

    # listen() activa el modo de escucha.
    # A partir de aquí el SO acepta conexiones en cola.
    server.listen()
    print(f'\n[*] Servidor TCP en escucha en ({HOST}:{PORT})\n')

    # accept() bloquea la ejecución hasta que llega una conexión.
    # Devuelve una tupla (socket_de_conexión, dirección_del_cliente).
    # El socket de conexión es DISTINTO del socket de servidor:
    # el servidor puede seguir aceptando nuevas conexiones mientras atiende esta.
    connection, address = server.accept()
    print(f'[+] Cliente conectado desde: {address[0]}:{address[1]}')

    # recv() recibe hasta N bytes. Bloquea hasta que llegan datos o se cierra la conexión.
    # Devuelve b'' (bytes vacíos) si el cliente cerró la conexión.
    data = connection.recv(1024)
    print(f"[<] Mensaje recibido: {data.decode('utf-8')}")

    # Se cierran ambos sockets: el de la conexión activa y el servidor principal
    server.close()
    connection.close()
    print('\n[*] Servidor cerrado.')


def start_server():
    """
    Versión recomendada: gestión de sockets con 'with'.
    Ambos sockets (servidor y conexión) se cierran automáticamente
    al salir de sus respectivos bloques 'with'.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # SO_REUSEADDR: permite reutilizar la dirección/puerto inmediatamente
        # tras cerrar el socket, evitando el error "Address already in use"
        # al reiniciar el servidor durante el desarrollo.
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((HOST, PORT))
        server.listen()
        print(f'\n[*] Servidor TCP en escucha en ({HOST}:{PORT})\n')

        # accept() devuelve el socket de la nueva conexión y la dirección del cliente.
        # El socket 'connection' gestiona exclusivamente la comunicación con ese cliente.
        connection, address = server.accept()

        # El socket de conexión también se puede usar como gestor de contexto
        with connection:
            print(f'[+] Cliente conectado desde: {address[0]}:{address[1]}')

            data = connection.recv(1024)
            print(f"[<] Mensaje recibido: {data.decode('utf-8')}")

        # 'connection' se cierra al salir de su 'with'
    # 'server' se cierra al salir de su 'with'
    print('\n[*] Servidor cerrado.')


# Punto de entrada del script
if __name__ == '__main__':
    start_server()