#!/usr/bin/env python3

import socket

# Dirección del servidor UDP al que enviaremos el datagrama
HOST = '127.0.0.1'
PORT = 4444


def start_udp_client():
    """
    Envía un único datagrama UDP al servidor y espera su respuesta.
    A diferencia de TCP, no se llama a connect(): sendto() envía
    directamente a la dirección de destino especificada en cada llamada.
    """
    # SOCK_DGRAM → tipo UDP (datagramas, sin conexión)
    # No hay three-way handshake ni estado de conexión que mantener
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        message = "Prueba de socket UDP"

        # sendto() envía los bytes al destino (HOST, PORT) sin necesidad
        # de haber establecido una conexión previa con connect().
        # El segundo argumento es siempre la dirección de destino.
        client.sendto(message.encode('utf-8'), (HOST, PORT))
        print(f"[>] Datagrama enviado a {HOST}:{PORT} → '{message}'")

        # recvfrom() devuelve el dato recibido Y la dirección del remitente.
        # Útil para saber quién respondió cuando se escucha en modo servidor.
        response, server_addr = client.recvfrom(1024)
        print(f"[<] Respuesta de {server_addr[0]}:{server_addr[1]} → '{response.decode('utf-8')}'")


# Punto de entrada del script
if __name__ == '__main__':
    start_udp_client()