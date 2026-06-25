#!/usr/bin/env python3

import socket

# Dirección del servidor al que nos queremos conectar
HOST = '127.0.0.1'
PORT = 4444


def start_client_v1():
    """
    Versión tradicional: el socket se abre y se cierra manualmente.
    Problema: si ocurre una excepción entre connect() y close(),
    el socket queda abierto indefinidamente (fuga de recursos).
    """
    server_addr = (HOST, PORT)   # empaquetamos host y puerto en una tupla
    print(f"\n[*] Intentando conectar a {server_addr[0]} en el puerto {server_addr[1]}...")

    # AF_INET     → familia de direcciones IPv4
    # SOCK_STREAM → tipo TCP (flujo de bytes orientado a conexión)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ejecuta el three-way handshake (SYN → SYN-ACK → ACK)
    client.connect(server_addr)
    print("[+] Conexión establecida con éxito!")

    # Los sockets trabajan con bytes, no con cadenas de texto.
    # encode('utf-8') convierte el str a bytes antes de enviarlo.
    message = "¡Hola servidor! Ya no soy Netcat, soy un script de Python."
    client.send(message.encode('utf-8'))
    print(f"[>] Mensaje enviado: '{message}'")

    # Cierre manual: depende de que el código llegue hasta aquí sin excepciones
    client.close()
    print("[*] Desconectado del servidor.")


def start_client():
    """
    Versión recomendada: el socket se gestiona con 'with'.
    El socket se cierra automáticamente al salir del bloque,
    incluso si se produce una excepción dentro de él.
    """
    server_addr = (HOST, PORT)
    print(f"\n[*] Intentando conectar a {server_addr[0]} en el puerto {server_addr[1]}...")

    # El bloque 'with' garantiza que client.close() se ejecute siempre
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(server_addr)
        print("[+] Conexión establecida con éxito!")

        message = "¡Hola servidor! Ya no soy Netcat, soy un script de Python."

        # send() puede enviar menos bytes de los solicitados si el buffer está lleno.
        # Para garantizar el envío completo, lo ideal es usar sendall() en su lugar.
        client.send(message.encode('utf-8'))
        print(f"[>] Mensaje enviado: '{message}'")

    # El socket ya fue cerrado automáticamente por el 'with'
    print("[*] Desconectado del servidor.")


# Punto de entrada del script
if __name__ == '__main__':
    start_client()