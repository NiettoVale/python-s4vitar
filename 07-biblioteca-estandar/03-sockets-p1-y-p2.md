# Sockets en Python: Conexiones de Red y Protocolos (Partes 1 y 2)

## Introducción

La programación de sockets es el pilar sobre el que se construye prácticamente cualquier comunicación de red a nivel de código. Un socket es, en esencia, un punto final de comunicación que permite a dos procesos —ubicados en la misma máquina o en máquinas distintas conectadas a través de una red— enviarse y recibirse datos. En ciberseguridad, los sockets son la base técnica de todo: un escáner de puertos, un listener para una shell reversa, un servidor de exfiltración de datos, un cliente que interactúa directamente con un servicio para probar vulnerabilidades, o una herramienta de análisis de tráfico a bajo nivel. Comprender cómo funcionan los sockets y cómo implementarlos en Python con el módulo `socket` es, por lo tanto, una habilidad absolutamente fundamental en el desarrollo de herramientas de seguridad.

## Protocolos de Transporte: TCP y UDP

Antes de abordar la implementación, es fundamental comprender los dos protocolos de transporte sobre los que operan los sockets: TCP y UDP. Ambos pertenecen a la capa de transporte del modelo OSI y del modelo TCP/IP, y la elección entre uno y otro determina el comportamiento de la comunicación.

### TCP: Transmission Control Protocol

TCP es un protocolo **orientado a la conexión**, lo que significa que antes de que pueda producirse ningún intercambio de datos, los dos extremos de la comunicación deben establecer explícitamente una conexión entre sí. Este proceso de establecimiento de conexión se conoce como el **Three-Way Handshake** (apretón de manos de tres vías):

1. **SYN**: el cliente envía al servidor un paquete con el flag SYN (*synchronize*) activado, indicando que desea iniciar una conexión y especificando un número de secuencia inicial.
2. **SYN-ACK**: el servidor responde con un paquete que tiene tanto el flag SYN como el ACK (*acknowledge*) activados, confirmando la recepción y respondiendo con su propio número de secuencia.
3. **ACK**: el cliente envía un último paquete de confirmación con el flag ACK, completando el establecimiento de la conexión.

Una vez establecida la conexión, TCP garantiza tres propiedades fundamentales que lo distinguen de UDP:

**Fiabilidad:** TCP garantiza que todos los paquetes llegarán a destino. Si algún paquete se pierde en el camino, el protocolo lo detecta automáticamente (mediante los números de secuencia y los mecanismos de ACK) y lo retransmite hasta que el destinatario lo recibe correctamente.

**Orden:** TCP garantiza que los datos llegan al destino en el mismo orden en que fueron enviados, incluso si los paquetes tomaron rutas distintas a través de la red y llegaron en un orden diferente. El receptor los reordena antes de entregarlos a la aplicación.

**Control de flujo y congestión:** TCP implementa mecanismos para evitar que el emisor envíe datos más rápido de lo que el receptor puede procesarlos (control de flujo), y para adaptar la velocidad de transmisión al estado de la red (control de congestión).

Todo esto tiene un costo: overhead. Cada paquete TCP lleva información adicional (flags, números de secuencia, checksums), y el protocolo requiere tiempo para el handshake inicial, los ACKs de confirmación y los mecanismos de retransmisión.

TCP es la elección correcta cuando la integridad y el orden de los datos son prioritarios: navegación web (HTTP/HTTPS), transferencia de archivos (FTP, SFTP), correo electrónico (SMTP, IMAP), SSH, bases de datos remotas.

### UDP: User Datagram Protocol

UDP es un protocolo **no orientado a la conexión**. No establece ningún canal previo antes de enviar datos: simplemente empaqueta los datos en un **datagrama** y lo envía hacia la dirección de destino, sin ninguna garantía de que llegue, de que llegue una sola vez, ni de que llegue en el orden correcto. No hay handshake, no hay ACKs, no hay retransmisiones.

Esta naturaleza "dispara y olvida" hace a UDP considerablemente más rápido y ligero que TCP. El emisor no espera ninguna confirmación, no mantiene estado de la conexión, y el header del datagrama UDP es mínimo (solo 8 bytes, frente a los 20 bytes mínimos de TCP).

UDP es la elección correcta cuando la velocidad prima sobre la fiabilidad: streaming de video y audio (donde un fotograma perdido es tolerable pero el retraso no lo es), juegos en línea en tiempo real, DNS (las consultas son tan cortas que la retransmisión si es necesario resulta más simple que establecer una conexión TCP), VoIP, y aplicaciones de telemetría o monitorización donde se envían actualizaciones periódicas y perder una de ellas es aceptable.

### Comparativa TCP vs UDP

| Característica | TCP | UDP |
|---|---|---|
| Tipo de conexión | Orientado a conexión | Sin conexión |
| Fiabilidad | Garantizada (retransmisión) | No garantizada |
| Orden de entrega | Garantizado | No garantizado |
| Velocidad | Más lento (overhead) | Más rápido (mínimo overhead) |
| Header | 20 bytes mínimo | 8 bytes |
| Control de flujo | Sí | No |
| Uso típico | Web, SSH, FTP, email | DNS, streaming, VoIP, juegos |
| Constante Python | `SOCK_STREAM` | `SOCK_DGRAM` |

## El Módulo `socket` de Python

El módulo `socket` de la biblioteca estándar de Python proporciona una API de bajo nivel para crear y manipular sockets, modelada directamente sobre la API de sockets de Berkeley POSIX que utiliza el propio sistema operativo. Esto significa que los conceptos que se aprenden aquí son transferibles directamente a la programación de redes en C, y que los sockets de Python se comportan de la misma forma que los sockets del sistema subyacente.

### Creación de un Socket

Un socket se crea con el constructor `socket.socket()`, que acepta dos argumentos principales: la **familia de direcciones** y el **tipo de socket**.

```python
import socket

# Familia de direcciones más comunes:
# socket.AF_INET   → IPv4 (la más habitual)
# socket.AF_INET6  → IPv6
# socket.AF_UNIX   → socket de dominio Unix (comunicación entre procesos locales)

# Tipos de socket:
# socket.SOCK_STREAM → TCP (flujo de bytes, orientado a conexión)
# socket.SOCK_DGRAM  → UDP (datagramas, sin conexión)

# Crear un socket TCP sobre IPv4
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Crear un socket UDP sobre IPv4
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

### Métodos Fundamentales del Socket

**`bind(address)`** — asocia el socket a una dirección (host, puerto) específica. Es necesario en el lado del servidor para indicar en qué dirección y puerto debe escuchar. El `host` puede ser `''` o `'0.0.0.0'` para escuchar en todas las interfaces disponibles, o una IP específica para escuchar solo en esa interfaz.

**`listen(backlog=None)`** — coloca el socket en modo de escucha (solo en TCP), indicando que está dispuesto a aceptar conexiones entrantes. El parámetro `backlog` define el número máximo de conexiones pendientes en la cola antes de que el sistema operativo comience a rechazarlas automáticamente.

**`accept()`** — bloquea la ejecución hasta que llega una conexión entrante, momento en el que devuelve una tupla `(connection, address)`, donde `connection` es un nuevo objeto socket específico para esa conexión con el cliente, y `address` es la dirección `(host, puerto)` del cliente.

**`connect(address)`** — en el lado del cliente TCP, establece la conexión con el servidor en la dirección `(host, puerto)` especificada, ejecutando el three-way handshake.

**`send(data)`** — envía los bytes proporcionados a través del socket. Devuelve el número de bytes realmente enviados, que puede ser menor que `len(data)` si el buffer del socket está lleno.

**`sendall(data)`** — igual que `send()`, pero repite las llamadas internamente hasta que todos los bytes han sido enviados, o lanza una excepción si ocurre un error.

**`sendto(data, address)`** — específico de UDP: envía los bytes al destino `(host, puerto)` especificado, sin requerir una conexión previa.

**`recv(bufsize)`** — recibe hasta `bufsize` bytes del socket y los devuelve como un objeto `bytes`. Si el buffer está vacío, bloquea hasta que lleguen datos. Si devuelve `b''` (bytes vacíos), indica que la conexión fue cerrada por el otro extremo.

**`recvfrom(bufsize)`** — específico de UDP: igual que `recv()`, pero devuelve una tupla `(data, address)` que incluye tanto los datos recibidos como la dirección del remitente.

**`close()`** — cierra el socket y libera los recursos asociados.

**`setsockopt(level, optname, value)`** — configura opciones del socket. La combinación más frecuente en servidores es `setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`, que permite reutilizar una dirección/puerto que todavía está en estado `TIME_WAIT` tras el cierre de la conexión anterior, evitando el error "Address already in use" al reiniciar un servidor durante el desarrollo.

## Manejadores de Contexto con Sockets: `with socket.socket() as s`

Al igual que con los archivos, los sockets deben cerrarse explícitamente cuando ya no son necesarios para liberar los recursos del sistema operativo que tienen asociados (descriptores de archivo, entradas en la tabla de conexiones del sistema). Si el socket no se cierra correctamente —por ejemplo, porque ocurrió una excepción antes de llegar a la llamada a `close()`—, el sistema operativo puede tardar un tiempo considerable en liberar esos recursos automáticamente, y en servidores de alto rendimiento esto puede provocar el agotamiento de los descriptores de archivo disponibles.

El patrón recomendado es siempre usar el gestor de contexto `with`, que garantiza que `socket.close()` se invocará automáticamente al salir del bloque, independientemente de si la salida fue normal o provocada por una excepción.

```python
import socket

# Forma tradicional: cierre manual, propenso a fugas si hay una excepción
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(("192.168.1.10", 443))
    s.sendall(b"GET / HTTP/1.0\r\n\r\n")
    data = s.recv(4096)
finally:
    s.close()  # se cierra siempre, pero obliga a usar try/finally

# Forma recomendada: gestor de contexto, cierre automático garantizado
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("192.168.1.10", 443))
    s.sendall(b"GET / HTTP/1.0\r\n\r\n")
    data = s.recv(4096)
# El socket se cierra automáticamente al salir del bloque with,
# haya ocurrido una excepción o no
```

## Diferencia entre `send()` y `sendall()`

Esta distinción es sutil pero crítica para escribir código de red robusto.

El método `send(data)` realiza **un único intento** de envío y devuelve el número de bytes que realmente pudo enviar en esa llamada. En condiciones de carga alta o cuando el buffer de envío del socket está lleno, este número puede ser **menor** que `len(data)`, lo que significa que no todos los datos fueron enviados. El código que invoca a `send()` debe verificar el valor de retorno y, si es menor que la longitud de los datos, llamar a `send()` de nuevo con el fragmento restante, repitiendo hasta que todos los datos hayan sido enviados.

```python
import socket

def send_all_manual(sock, data):
    """Implementación manual del comportamiento de sendall() usando send()."""
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("La conexión fue cerrada por el otro extremo")
        total_sent += sent
    return total_sent
```

El método `sendall(data)`, en cambio, implementa internamente exactamente este bucle: sigue llamando a `send()` con el fragmento pendiente hasta que la totalidad de los datos ha sido enviada, o lanza una excepción si ocurre un error durante el proceso. No devuelve el número de bytes enviados (devuelve `None` al completarse con éxito), ya que la garantía implícita es que o se enviaron todos o se lanzó una excepción.

```python
# Con send(): hay que manejar el envío parcial manualmente
bytes_sent = sock.send(data)
if bytes_sent < len(data):
    # Datos no enviados completamente: hay que reenviar el resto
    sock.send(data[bytes_sent:])   # aún simplificado: en la realidad necesita un bucle

# Con sendall(): envío garantizado o excepción
sock.sendall(data)   # o se enviaron todos los bytes, o se lanzó una excepción
```

**¿Cuándo usar cada uno?** En la práctica, `sendall()` es la opción correcta para la gran mayoría de los casos en que se quiere enviar un bloque de datos completo a través de un socket TCP. `send()` resulta apropiado en escenarios de bajo nivel donde se necesita un control granular sobre el proceso de envío, por ejemplo en implementaciones de protocolos no bloqueantes o en código donde se debe responder a eventos del sistema operativo entre fragmentos de envío.

## Arquitectura Cliente-Servidor con TCP

La arquitectura más habitual para aplicaciones TCP es la arquitectura cliente-servidor: un proceso actúa como **servidor**, que se mantiene en escucha esperando conexiones entrantes, y uno o varios procesos actúan como **clientes**, que inician la conexión hacia el servidor.

El flujo de operaciones difiere significativamente entre el servidor y el cliente:

**Servidor TCP:**
1. Crear el socket (`socket()`)
2. Configurar opciones (`setsockopt()`) — opcional pero recomendable
3. Vincular a dirección y puerto (`bind()`)
4. Activar modo escucha (`listen()`)
5. Aceptar conexiones entrantes (`accept()`) → devuelve un socket de conexión
6. Recibir y enviar datos (`recv()`, `send()`/`sendall()`)
7. Cerrar la conexión (`close()`)

**Cliente TCP:**
1. Crear el socket (`socket()`)
2. Conectar al servidor (`connect()`)
3. Enviar y recibir datos (`send()`/`sendall()`, `recv()`)
4. Cerrar la conexión (`close()`)

```python
# ─── Servidor TCP ────────────────────────────────────────────
import socket

HOST = "127.0.0.1"
PORT = 4444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # SO_REUSEADDR evita el error "Address already in use" al reiniciar el servidor
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Servidor en escucha en {HOST}:{PORT}")

    conn, addr = server.accept()
    with conn:
        print(f"[+] Conexión aceptada desde {addr[0]}:{addr[1]}")
        data = conn.recv(1024)
        print(f"[*] Datos recibidos: {data.decode('utf-8')}")
        conn.sendall(b"ACK: mensaje recibido")
```

```python
# ─── Cliente TCP ─────────────────────────────────────────────
import socket

HOST = "127.0.0.1"
PORT = 4444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print(f"[+] Conectado a {HOST}:{PORT}")

    client.sendall("Hola servidor, soy un cliente Python".encode("utf-8"))
    print("[*] Mensaje enviado")

    response = client.recv(1024)
    print(f"[*] Respuesta del servidor: {response.decode('utf-8')}")
```

## Comunicación UDP con Sockets

En UDP no existe el concepto de conexión: el cliente simplemente envía datagramas a la dirección del servidor, y el servidor los recibe de cualquier origen. Esto simplifica ligeramente el código del servidor (no hay `listen()` ni `accept()`), pero implica que el servidor debe identificar al remitente de cada datagrama a través del valor de retorno de `recvfrom()`.

**Servidor UDP:**
1. Crear el socket con `SOCK_DGRAM`
2. Vincular a dirección y puerto (`bind()`)
3. Recibir datagramas (`recvfrom()`) — devuelve `(data, address)`
4. Responder al remitente si es necesario (`sendto()`)

**Cliente UDP:**
1. Crear el socket con `SOCK_DGRAM`
2. Enviar datagramas al servidor (`sendto()`)
3. Recibir respuesta si se espera una (`recvfrom()`)

```python
# ─── Servidor UDP ────────────────────────────────────────────
import socket

HOST = "127.0.0.1"
PORT = 4444

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    print(f"[*] Servidor UDP en escucha en {HOST}:{PORT}")

    while True:
        data, address = server.recvfrom(1024)
        print(f"[+] Datagrama recibido de {address[0]}:{address[1]}")
        print(f"[*] Contenido: {data.decode('utf-8')}")
        # Responder al remitente
        server.sendto(b"Datagrama recibido", address)
```

```python
# ─── Cliente UDP ─────────────────────────────────────────────
import socket

HOST = "127.0.0.1"
PORT = 4444

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    message = "Datagrama de prueba desde cliente UDP"
    client.sendto(message.encode("utf-8"), (HOST, PORT))
    print(f"[*] Datagrama enviado a {HOST}:{PORT}")

    # Esperar respuesta del servidor (opcional en UDP)
    response, server_addr = client.recvfrom(1024)
    print(f"[*] Respuesta de {server_addr}: {response.decode('utf-8')}")
```

## Opciones del Socket y Configuraciones de Timeout

Además de `SO_REUSEADDR`, el módulo `socket` permite configurar otras opciones relevantes para el trabajo en ciberseguridad:

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Permitir reutilizar la dirección inmediatamente tras cerrar el socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Establecer un timeout: si recv() o connect() tardan más de N segundos
    # sin recibir datos, se lanzará socket.timeout
    s.settimeout(3.0)

    # Poner el socket en modo no bloqueante:
    # recv() y accept() retornan inmediatamente con BlockingIOError si no hay datos
    # (generalmente se prefiere el timeout sobre el modo no bloqueante puro)
    # s.setblocking(False)

    try:
        s.connect(("192.168.1.10", 22))
        banner = s.recv(1024)
        print(f"Banner SSH: {banner.decode('utf-8', errors='ignore').strip()}")
    except socket.timeout:
        print("Tiempo de espera agotado — el host no respondió")
    except ConnectionRefusedError:
        print("Conexión rechazada — el puerto está cerrado")
    except OSError as error:
        print(f"Error de red: {error}")
```

## Resolución de Nombres y Utilidades del Módulo `socket`

El módulo `socket` incluye también varias funciones de utilidad para la resolución de nombres de host, conversión de formatos de dirección y obtención de información del sistema:

```python
import socket

# Resolver un nombre de host a su dirección IP
ip = socket.gethostbyname("empresa.com")
print(f"IP de empresa.com: {ip}")

# Obtener toda la información de dirección: familia, tipo, protocolo, nombre canónico, IPs
info = socket.getaddrinfo("empresa.com", 443)
for entry in info:
    print(entry)

# Obtener el nombre del host local
hostname = socket.gethostname()
print(f"Nombre del host local: {hostname}")

# Obtener la IP del host local
local_ip = socket.gethostbyname(socket.gethostname())
print(f"IP local: {local_ip}")

# Convertir un número de puerto a su nombre de servicio conocido
service = socket.getservbyport(443, "tcp")
print(f"Puerto 443/tcp: {service}")   # https
```

## Buenas Prácticas

Siempre debe usarse el gestor de contexto `with socket.socket() as s` en lugar de crear el socket y cerrarlo manualmente, ya que garantiza que el socket se cierre correctamente incluso ante excepciones. Siempre debe configurarse `SO_REUSEADDR` en los sockets de servidor para evitar el error "Address already in use" al reiniciar el proceso durante el desarrollo o ante reinicios rápidos en producción.

En lo que respecta al envío de datos, `sendall()` debe preferirse sobre `send()` en todos aquellos casos en que se quiere garantizar la entrega completa de un bloque de datos a través de un socket TCP, reservando `send()` para implementaciones de bajo nivel con control granular del proceso de envío. Siempre debe configurarse un timeout con `settimeout()` cuando se trabaja con sockets que se conectan a hosts remotos no controlados, para evitar que el programa quede bloqueado indefinidamente ante un host que no responde.

Los datos enviados y recibidos a través de sockets son siempre de tipo `bytes`, no cadenas de texto: toda cadena debe codificarse antes de enviarse (`.encode("utf-8")`) y decodificarse tras recibirla (`.decode("utf-8")`). Ante datos de red de origen desconocido, el uso de `errors="ignore"` o `errors="replace"` en el `decode()` previene excepciones ante bytes inválidos para la codificación especificada.