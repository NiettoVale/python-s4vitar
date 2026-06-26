# Sockets en Python: `setsockopt` y Concurrencia con `threading` (Partes 3 y 4)

## Parte 3: Configuración Avanzada de Sockets con `setsockopt()`

### ¿Qué es `setsockopt()`?

La función `setsockopt()` permite ajustar el comportamiento de un socket modificando sus opciones de configuración internas. Cuando se crea un socket con `socket.socket()`, este viene con un conjunto de valores por defecto que son razonables para la mayoría de los casos, pero que en situaciones específicas pueden resultar inadecuados: un servidor que no puede reutilizar su puerto tras un reinicio, una conexión que no detecta automáticamente que el otro extremo se cayó, o un buffer de recepción demasiado pequeño para los volúmenes de datos esperados. `setsockopt()` es la herramienta que permite cambiar todos estos parámetros de forma precisa.

Su firma es la siguiente:

```python
socket.setsockopt(level, optname, value)
```

Donde `level` indica a qué capa del stack de red pertenece la opción, `optname` es el identificador de la opción específica a configurar, y `value` es el valor a establecer (generalmente `0` o `1` para opciones booleanas, o un entero para parámetros numéricos).

### Niveles de Configuración

El parámetro `level` de `setsockopt()` determina el **ámbito** al que se aplica la opción, es decir, a qué capa del stack de red afecta el ajuste. Python expone los niveles más comunes como constantes del módulo `socket`.

#### `socket.SOL_SOCKET`: Nivel de Socket

`SOL_SOCKET` es el nivel más genérico: las opciones configuradas en este nivel afectan al comportamiento del socket en sí mismo, de forma independiente del protocolo de transporte que esté utilizando (TCP, UDP, u otro). Son opciones que el sistema operativo aplica a toda operación realizada a través del socket.

```python
import socket

# Todas las opciones con SOL_SOCKET aplican sin importar si el socket es TCP o UDP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

#### `socket.IPPROTO_TCP`: Nivel de Protocolo TCP

`IPPROTO_TCP` es el nivel específico para opciones del protocolo TCP. Las opciones configuradas en este nivel solo tienen sentido para sockets TCP y controlan aspectos del comportamiento particular de ese protocolo.

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # TCP_NODELAY desactiva el algoritmo de Nagle: envía datos inmediatamente
    # en lugar de acumularlos para optimizar el número de segmentos TCP.
    # Útil cuando la latencia importa más que el throughput (ej: shells interactivas).
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
```

### Opciones Comunes de `SOL_SOCKET`

#### `SO_REUSEADDR`: Reutilización Inmediata de Dirección y Puerto

Es la opción de `setsockopt()` más utilizada en el desarrollo de servidores, y la más importante de conocer. Para entender por qué existe, es necesario comprender el estado `TIME_WAIT` del protocolo TCP.

Cuando una conexión TCP se cierra, el sistema operativo no libera inmediatamente el par (dirección, puerto) que estaba usando. En su lugar, mantiene el socket en un estado denominado `TIME_WAIT` durante un período de tiempo (típicamente entre 30 segundos y 4 minutos, dependiendo del sistema operativo) para garantizar que todos los paquetes retrasados de la conexión anterior hayan tenido tiempo suficiente para llegar y ser descartados, evitando así que una nueva conexión en el mismo puerto los interprete como datos suyos.

El problema surge durante el desarrollo o ante reinicios rápidos de un servidor: si el proceso del servidor se detiene y se intenta reiniciarlo inmediatamente, el sistema operativo rechazará el `bind()` en el mismo puerto con el error `OSError: [Errno 98] Address already in use`, porque el socket anterior todavía está en `TIME_WAIT`.

`SO_REUSEADDR` le indica al sistema operativo que está bien reutilizar ese par (dirección, puerto) aunque todavía esté en `TIME_WAIT`, permitiendo que el servidor se reinicie inmediatamente.

```python
import socket

HOST = "0.0.0.0"
PORT = 4444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Debe establecerse ANTES de bind(), ya que es bind() el que reserva el puerto
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Servidor en escucha en {HOST}:{PORT}")
    # ...
```

**¿Cuándo usarlo?** Prácticamente siempre en servidores, especialmente durante el desarrollo. Es una opción de tan bajo riesgo y tan alto beneficio en conveniencia que se considera una buena práctica incluirla por defecto en todo socket de servidor.

#### `SO_REUSEPORT`: Reutilización de Puerto entre Procesos

`SO_REUSEPORT` (disponible en Linux 3.9+ y macOS) va un paso más allá que `SO_REUSEADDR`: permite que múltiples procesos o hilos, incluso de programas distintos, hagan `bind()` en el mismo par (dirección, puerto) simultáneamente. El kernel distribuye las conexiones entrantes entre todos los sockets vinculados al mismo puerto, lo que permite implementar balanceo de carga a nivel de SO sin necesidad de un proceso coordinador.

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.bind(("0.0.0.0", 8080))
    server.listen()
```

#### `SO_KEEPALIVE`: Detección de Conexiones Caídas

`SO_KEEPALIVE` activa el mecanismo de *keepalive* a nivel TCP: el sistema operativo envía periódicamente paquetes de prueba a través de la conexión para verificar que el otro extremo sigue vivo. Si no recibe respuesta tras un número configurable de intentos, cierra la conexión y notifica al proceso. Esto es fundamental en servidores de larga duración para detectar clientes que se desconectaron de forma abrupta (por ejemplo, por un corte de red) sin haber enviado un paquete de cierre `FIN`.

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    # En Linux es posible configurar los parámetros específicos del keepalive:
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)   # segundos inactivos antes del primer keepalive
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)  # intervalo entre keepalives
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)     # número de intentos antes de cerrar
```

#### `SO_RCVBUF` y `SO_SNDBUF`: Tamaño de los Buffers

`SO_RCVBUF` y `SO_SNDBUF` controlan el tamaño del buffer de recepción y de envío del socket, respectivamente. Aumentar el tamaño del buffer puede mejorar el rendimiento en transferencias de grandes volúmenes de datos, ya que el sistema operativo puede acumular más datos antes de que la aplicación los procese.

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Consultar el tamaño actual del buffer de recepción
    current_rcvbuf = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print(f"Buffer de recepción actual: {current_rcvbuf} bytes")

    # Establecer un buffer más grande para transferencias de archivos
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)   # 64 KB
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)   # 64 KB
```

#### `SO_TIMEOUT` vs `settimeout()`: Dos Formas de Configurar Timeouts

El timeout de un socket puede configurarse a través de `setsockopt()` con la opción `SO_RCVTIMEO` y `SO_SNDTIMEO`, o de forma más sencilla mediante el método `settimeout()` que ofrece Python directamente sobre el objeto socket. Ambos enfoques producen el mismo resultado, pero `settimeout()` es la forma idiomática y recomendada en Python.

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Forma idiomática en Python: timeout de 5 segundos para todas las operaciones
    s.settimeout(5.0)

    try:
        s.connect(("192.168.1.10", 22))
        banner = s.recv(1024)
    except socket.timeout:
        print("[!] Tiempo de espera agotado")
    except ConnectionRefusedError:
        print("[!] Conexión rechazada: puerto cerrado")
```

### Consultar Opciones con `getsockopt()`

El complemento de `setsockopt()` es `getsockopt()`, que permite leer el valor actual de cualquier opción del socket, tanto para inspección como para diagnóstico.

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    reuse = s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    keepalive = s.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    rcvbuf = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    sndbuf = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

    print(f"SO_REUSEADDR : {bool(reuse)}")
    print(f"SO_KEEPALIVE : {bool(keepalive)}")
    print(f"SO_RCVBUF    : {rcvbuf} bytes")
    print(f"SO_SNDBUF    : {sndbuf} bytes")
```

---

## Parte 4: Servidores Concurrentes con `threading`

### El Problema del Servidor de Un Solo Hilo

La implementación básica de un servidor TCP que se vio en las partes anteriores tiene una limitación fundamental: solo puede atender a **un cliente a la vez**. Una vez que acepta una conexión con `accept()` y comienza a procesar los datos de ese cliente con `recv()`, el servidor queda bloqueado esperando que ese cliente termine, sin poder atender a ningún otro cliente que intente conectarse en ese mismo momento.

En el contexto de una herramienta de ciberseguridad, esto puede ser un problema serio: un listener de shell reversa que solo puede manejar una sesión activa a la vez, un servidor de exfiltración que pierde datos de otros agentes mientras procesa uno, o un honeypot que no puede registrar conexiones simultáneas de múltiples atacantes.

```python
# Servidor de un solo hilo: el ciclo de vida completo
# accept() → procesar cliente → accept() → procesar cliente → ...
# Solo un cliente puede ser atendido en cada momento
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("0.0.0.0", 4444))
    server.listen()
    while True:
        conn, addr = server.accept()   # espera una conexión
        handle_client(conn, addr)      # bloquea hasta que este cliente termine
        # El siguiente cliente no puede conectarse hasta que handle_client() retorne
```

### La Solución: `threading`

El módulo `threading` de la biblioteca estándar de Python permite crear y gestionar **hilos de ejecución** (*threads*): flujos de ejecución independientes que comparten el mismo espacio de memoria del proceso pero corren de forma concurrente. Al delegar el procesamiento de cada cliente a un hilo independiente, el hilo principal del servidor puede volver inmediatamente a `accept()` y quedar disponible para la siguiente conexión, sin esperar a que el cliente anterior haya terminado.

```python
import socket
import threading

def handle_client(conn, addr):
    """Esta función se ejecuta en un hilo separado para cada cliente."""
    with conn:
        print(f"[+] Cliente conectado: {addr[0]}:{addr[1]}")
        while True:
            data = conn.recv(1024)
            if not data:   # b'' indica que el cliente cerró la conexión
                break
            conn.sendall(data)   # eco: reenvía los datos recibidos al cliente
        print(f"[-] Cliente desconectado: {addr[0]}:{addr[1]}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 4444))
    server.listen()
    print("[*] Servidor multihilo en escucha en 0.0.0.0:4444")

    while True:
        conn, addr = server.accept()   # acepta la conexión

        # Crear un nuevo hilo para atender a este cliente.
        # target: función a ejecutar en el nuevo hilo
        # args: argumentos a pasar a esa función
        # daemon=True: el hilo se detendrá automáticamente cuando el proceso principal termine
        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        client_thread.start()
        # El servidor vuelve inmediatamente al accept() sin esperar que el hilo termine
```

### Anatomía de un Hilo con `threading.Thread`

La clase `threading.Thread` es la forma principal de crear hilos en Python. Sus parámetros más relevantes son:

**`target`**: la función que debe ejecutar el hilo cuando arranque.

**`args`**: tupla con los argumentos posicionales a pasar a la función `target`.

**`kwargs`**: diccionario con los argumentos por clave a pasar a la función `target`.

**`daemon`**: si es `True`, el hilo es un **hilo demonio**: cuando el hilo principal del programa termina, todos los hilos demonio son eliminados automáticamente, sin necesidad de esperar a que completen su trabajo. Si es `False` (por defecto), el programa no termina hasta que todos los hilos no demonio hayan finalizado. En servidores donde los hilos de cliente pueden vivir mucho tiempo, establecer `daemon=True` es generalmente lo correcto para que Ctrl+C detenga el servidor limpiamente.

```python
import threading
import time

def worker(worker_id, delay):
    """Función que ejecutará cada hilo."""
    print(f"[Hilo {worker_id}] Iniciado")
    time.sleep(delay)   # simula procesamiento
    print(f"[Hilo {worker_id}] Finalizado tras {delay}s")

# Crear múltiples hilos
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i, i + 1), daemon=True)
    threads.append(t)
    t.start()   # arranca el hilo

# start() no bloquea: el código continúa inmediatamente
print("[Principal] Todos los hilos iniciados, hilo principal continúa")

# join() bloquea el hilo principal hasta que el hilo especificado termine
for t in threads:
    t.join()
print("[Principal] Todos los hilos han terminado")
```

### Sincronización: `threading.Lock`

Los hilos de un mismo proceso comparten la memoria, lo que significa que pueden acceder y modificar las mismas variables. Si dos hilos modifican concurrentemente la misma estructura de datos sin ningún mecanismo de coordinación, pueden producirse **condiciones de carrera** (*race conditions*): situaciones en las que el resultado final depende del orden de ejecución impredecible de los hilos, generando resultados incorrectos o corrupción de datos.

La herramienta principal para prevenir esto es el `Lock` (*mutex*): un objeto que garantiza que, en cualquier momento, como máximo un hilo puede estar ejecutando el código protegido por el lock. El patrón es siempre: adquirir el lock antes del bloque crítico, ejecutar el bloque, liberar el lock. El uso con el gestor de contexto `with lock:` garantiza la liberación automática incluso ante excepciones.

```python
import socket
import threading

# Estructura compartida entre todos los hilos del servidor
connected_clients = []
clients_lock = threading.Lock()   # protege el acceso a connected_clients


def handle_client(conn, addr):
    """Gestiona la comunicación con un cliente en un hilo independiente."""
    client_info = f"{addr[0]}:{addr[1]}"

    # Sección crítica: modificar la lista compartida de forma segura
    with clients_lock:
        connected_clients.append(client_info)
        print(f"[+] {client_info} conectado | Total activos: {len(connected_clients)}")

    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data.upper())   # responde con los datos en mayúsculas
    finally:
        # Sección crítica: eliminar el cliente al desconectarse
        with clients_lock:
            connected_clients.remove(client_info)
            print(f"[-] {client_info} desconectado | Total activos: {len(connected_clients)}")
```

### Variables de Condición y Eventos entre Hilos

Además del `Lock`, el módulo `threading` ofrece otros mecanismos de sincronización:

**`threading.Event`**: permite que un hilo señalice a otros que ha ocurrido algo. Un hilo llama a `event.set()` para activar la señal, y otros hilos pueden esperar con `event.wait()` hasta que la señal se active. Es útil para implementar mecanismos de parada coordinada.

```python
import threading
import socket

stop_event = threading.Event()   # señal de parada compartida entre hilos

def handle_client(conn, addr):
    with conn:
        while not stop_event.is_set():   # el hilo verifica si debe detenerse
            conn.settimeout(1.0)
            try:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
            except socket.timeout:
                continue   # el timeout permite revisar stop_event periódicamente

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", 4444))
        server.listen()
        try:
            while not stop_event.is_set():
                server.settimeout(1.0)
                try:
                    conn, addr = server.accept()
                    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\n[!] Deteniendo servidor...")
            stop_event.set()   # señaliza a todos los hilos que deben detenerse
```

### `threading.Semaphore`: Limitar la Cantidad de Clientes Simultáneos

Un `Semaphore` es similar a un `Lock`, pero permite que hasta N hilos accedan concurrentemente al recurso protegido, en lugar de solo uno. En el contexto de un servidor, puede usarse para limitar el número máximo de clientes conectados simultáneamente, evitando que el servidor sea sobrecargado.

```python
import threading
import socket

MAX_CLIENTS = 10
client_semaphore = threading.Semaphore(MAX_CLIENTS)

def handle_client(conn, addr):
    with client_semaphore:   # adquiere el semáforo: reduce el contador en 1
        # Si ya hay MAX_CLIENTS conectados, este hilo bloquea aquí hasta que uno se desconecte
        try:
            with conn:
                data = conn.recv(1024)
                conn.sendall(data)
        except Exception as error:
            print(f"[!] Error con {addr}: {error}")
    # Al salir del 'with', el semáforo se libera: el contador vuelve a subir
```

### El GIL y sus Implicaciones para `threading`

Python implementa el **GIL** (*Global Interpreter Lock*): un mutex interno del intérprete que garantiza que solo un hilo de Python puede ejecutar bytecode en un momento dado, incluso en sistemas con múltiples núcleos de CPU. Esto significa que el `threading` de Python **no proporciona paralelismo real** para código ligado a la CPU (*CPU-bound*): si todos los hilos realizan cálculos intensivos, en la práctica se ejecutan de forma pseudoparalela, alternándose el acceso al intérprete.

Sin embargo, para código de red (*I/O-bound*), como es el caso de los servidores de sockets, el GIL no es un problema significativo: cuando un hilo está bloqueado esperando datos de la red en `recv()` o `accept()`, el GIL se libera automáticamente, permitiendo que otros hilos ejecuten su código. En la práctica, un servidor TCP multihilo en Python puede atender miles de conexiones simultáneas de forma eficiente, porque la mayor parte del tiempo de cada hilo se pasa esperando datos de la red, no ejecutando código Python.

```
# Escenario típico de un hilo de cliente en un servidor TCP:
#
# recv()  ←→  [BLOQUEADO esperando datos de red]  ←→  GIL liberado
#    ↓
# procesar datos recibidos  ←→  [ejecutando Python]  ←→  GIL adquirido
#    ↓
# sendall()  ←→  [BLOQUEADO enviando datos por red]  ←→  GIL liberado
#    ↓
# recv()  ←→  [BLOQUEADO esperando datos de red]  ←→  GIL liberado
```

Para aplicaciones que necesitan paralelismo real a nivel de CPU, la alternativa es el módulo `multiprocessing`, que usa procesos separados en lugar de hilos, evitando así el GIL.

### Alternativas a `threading`: Cuándo Considerar Otras Aproximaciones

Si bien `threading` es la solución más directa y simple para gestionar múltiples clientes, existen alternativas que resultan más apropiadas en ciertos escenarios:

**`concurrent.futures.ThreadPoolExecutor`**: proporciona una interfaz de más alto nivel para gestionar un pool de hilos, reutilizando los hilos en lugar de crear uno nuevo por cada cliente, lo que reduce el overhead para servidores con muy alta frecuencia de conexiones.

```python
from concurrent.futures import ThreadPoolExecutor
import socket

MAX_WORKERS = 50   # máximo 50 hilos activos simultáneamente

def handle_client(conn_addr):
    conn, addr = conn_addr
    with conn:
        data = conn.recv(1024)
        if data:
            conn.sendall(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 4444))
    server.listen()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        while True:
            conn, addr = server.accept()
            pool.submit(handle_client, (conn, addr))
```

**`asyncio`**: para servidores que deben manejar un número muy elevado de conexiones simultáneas (miles o decenas de miles), la programación asíncrona con `asyncio` ofrece mejor escalabilidad que `threading`, ya que gestiona múltiples conexiones dentro de un único hilo mediante un bucle de eventos, sin el overhead de crear y gestionar múltiples hilos del sistema operativo.

## Buenas Prácticas en Servidores Multihilo

Siempre establecer `daemon=True` en los hilos de cliente para garantizar que el servidor pueda detenerse limpiamente con Ctrl+C sin quedar bloqueado esperando que todos los hilos terminen. Proteger siempre el acceso a cualquier estructura de datos compartida entre hilos con un `Lock`, incluyendo listas de clientes conectados, contadores de conexiones, o cachés compartidas, para evitar condiciones de carrera.

Configurar siempre un timeout con `settimeout()` en los sockets de cliente dentro de los hilos, para evitar que un cliente que deja de responder bloquee su hilo indefinidamente. Usar `ThreadPoolExecutor` en lugar de crear hilos ilimitados cuando la tasa de conexiones puede ser muy alta, ya que crear un hilo del sistema operativo por cada conexión tiene un costo no despreciable y puede agotar los recursos del sistema ante ataques de tipo *connection flood*.

Capturar siempre las excepciones dentro de la función de cada hilo con un bloque `try/except` genérico, para evitar que un error en el procesamiento de un cliente derribe el hilo sin liberar sus recursos (el socket de conexión) y sin notificar al servidor de que ese cliente ya no está siendo atendido.