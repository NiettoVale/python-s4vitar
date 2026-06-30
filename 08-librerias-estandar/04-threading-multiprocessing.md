# Concurrencia y Paralelismo en Python: `threading` y `multiprocessing`

## Introducción

Python ofrece dos módulos principales para ejecutar código de forma simultánea: `threading` y `multiprocessing`. Aunque ambos permiten que un programa realice varias tareas a la vez, lo hacen de maneras fundamentalmente distintas, con implicaciones muy diferentes en rendimiento, uso de memoria, y complejidad. Comprender cuándo usar cada uno —y por qué— es una habilidad esencial para construir herramientas de ciberseguridad eficientes, especialmente cuando se trata de operaciones que pueden beneficiarse de la concurrencia, como escanear múltiples hosts en paralelo, probar credenciales concurrentemente, o procesar grandes volúmenes de logs.

## El Global Interpreter Lock (GIL): el Concepto Central

Antes de entrar en los detalles de cada módulo, es imprescindible entender el **GIL** (_Global Interpreter Lock_), porque es precisamente la existencia del GIL lo que determina cuándo `threading` es suficiente y cuándo es necesario recurrir a `multiprocessing`.

El GIL es un mutex interno del intérprete CPython (la implementación estándar de Python) que garantiza que, en cualquier momento dado, solo **un hilo de Python puede ejecutar bytecode**, incluso en un sistema con múltiples núcleos de CPU. El GIL existe por razones históricas de diseño interno: simplifica la gestión de memoria de CPython, ya que el conteo de referencias usado para el recolector de basura no necesita ser thread-safe si solo un hilo puede ejecutarse a la vez.

Las consecuencias prácticas del GIL son las siguientes:

Para código **ligado a CPU** (_CPU-bound_): el GIL es un problema real. Si se tienen cuatro hilos haciendo cálculos intensivos en un sistema de cuatro núcleos, en la práctica no obtendrán ningún beneficio de los cuatro núcleos: el GIL garantiza que solo uno ejecuta Python en cada momento, alternándose el acceso al intérprete. En este escenario, `threading` no proporciona paralelismo real.

Para código **ligado a E/S** (_I/O-bound_): el GIL no es un problema significativo. Cuando un hilo realiza una operación de E/S (esperar datos de la red, leer un archivo del disco, esperar en `recv()`), el GIL se **libera automáticamente**, permitiendo que otros hilos ejecuten su código Python mientras el primero está bloqueado esperando. Esto hace que `threading` sea perfectamente adecuado para servidores de red, escaners de puertos, clientes HTTP concurrentes, y en general cualquier herramienta donde la mayor parte del tiempo se pasa esperando respuestas externas.

```
# Representación del comportamiento del GIL:
#
# CPU-bound (threading NO ayuda):
# Hilo 1: [computar] GIL → [computar] GIL → [computar]
# Hilo 2:              espera GIL → [computar] espera GIL
# → No hay paralelismo real, puede ser incluso más lento que un solo hilo
#
# I/O-bound (threading SÍ ayuda):
# Hilo 1: [recv()... GIL liberado ...] [computar] [recv()... GIL liberado ...]
# Hilo 2:               [computar] [recv()... GIL liberado ...] [computar]
# → Los hilos se ejecutan genuinamente en paralelo durante las esperas de I/O
```

---

## La Biblioteca `threading`

### Creación y Ciclo de Vida de un Hilo

La clase principal de la biblioteca `threading` es `threading.Thread`. Un hilo se crea instanciando esta clase con la función a ejecutar (`target`) y sus argumentos (`args` o `kwargs`), y se inicia con el método `start()`. Una vez iniciado, el hilo ejecuta su función en segundo plano mientras el hilo principal continúa su propia ejecución.

```python
import threading
import time

def scan_host(host, port, timeout=2):
    """Simula el escaneo de un puerto en un host."""
    print(f"  [Hilo {threading.current_thread().name}] Escaneando {host}:{port}...")
    time.sleep(timeout)   # simula la espera de respuesta de la red
    print(f"  [Hilo {threading.current_thread().name}] Escaneo de {host}:{port} completado")

# Crear hilos: target es la función, args es la tupla de argumentos
thread_1 = threading.Thread(target=scan_host, args=("192.168.1.10", 22),   name="T-1")
thread_2 = threading.Thread(target=scan_host, args=("192.168.1.11", 443),  name="T-2")
thread_3 = threading.Thread(target=scan_host, args=("192.168.1.12", 3389), name="T-3")

# start() lanza el hilo; la ejecución continúa inmediatamente sin esperar
thread_1.start()
thread_2.start()
thread_3.start()

print("  [Principal] Todos los hilos iniciados, el hilo principal continúa...")

# join() bloquea el hilo que lo llama hasta que el hilo especificado termine
thread_1.join()
thread_2.join()
thread_3.join()

print("  [Principal] Todos los hilos han finalizado")
```

### Hilos Demonio (`daemon=True`)

Un **hilo demonio** se detiene automáticamente cuando el hilo principal del programa termina, sin importar si el hilo demonio ha completado su trabajo. Los hilos no demonio, en cambio, impiden que el programa termine hasta que ellos mismos finalicen. En el contexto de servidores o herramientas de largo plazo, `daemon=True` permite que Ctrl+C detenga el programa limpiamente sin quedar bloqueado esperando que los hilos de cliente terminen.

```python
import threading
import time

def background_monitor():
    """Hilo demonio que monitoriza continuamente."""
    while True:
        print("  [Monitor] Verificando estado del sistema...")
        time.sleep(2)

# daemon=True: este hilo se detiene cuando el programa principal termina
monitor = threading.Thread(target=background_monitor, daemon=True, name="Monitor")
monitor.start()

# El programa principal hace su trabajo...
time.sleep(5)
print("  [Principal] Trabajo completado, terminando...")
# Al salir, el hilo demonio se detiene automáticamente (aunque esté en un while True)
```

### Sincronización con `threading.Lock`

Dado que los hilos comparten el mismo espacio de memoria, acceder y modificar concurrentemente las mismas estructuras de datos puede producir **condiciones de carrera**: situaciones en que el resultado final depende del orden de ejecución impredecible de los hilos. El `Lock` es el mecanismo básico de sincronización: garantiza exclusión mutua, es decir, que en cualquier momento como máximo un hilo puede estar ejecutando el código protegido.

```python
import threading

found_hosts = []
results_lock = threading.Lock()   # protege el acceso a found_hosts

def probe_host(host, results_list, lock):
    """Sonda un host y añade el resultado a la lista compartida de forma segura."""
    # Sección crítica: el lock garantiza que dos hilos no modifiquen la lista al mismo tiempo
    with lock:
        results_list.append({"host": host, "status": "active"})
        print(f"  [+] Host {host} añadido (total: {len(results_list)})")

threads = []
hosts_to_scan = [f"192.168.1.{i}" for i in range(1, 6)]

for host in hosts_to_scan:
    t = threading.Thread(target=probe_host, args=(host, found_hosts, results_lock))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\n  Total de hosts registrados: {len(found_hosts)}")
```

### `threading.Semaphore`: Limitar la Concurrencia

Un `Semaphore` extiende el concepto del `Lock` permitiendo que hasta N hilos accedan concurrentemente al recurso protegido, en lugar de solo uno. En el contexto de un scanner, permite limitar el número de conexiones simultáneas para no sobrecargar el objetivo ni agotar los recursos locales.

```python
import threading
import time

MAX_CONCURRENT = 3
sem = threading.Semaphore(MAX_CONCURRENT)

def limited_scan(host):
    """El semáforo garantiza un máximo de MAX_CONCURRENT escaneos simultáneos."""
    with sem:   # adquiere el semáforo (bloquea si ya hay MAX_CONCURRENT hilos dentro)
        print(f"  [Escaneando] {host} (hilos activos: {MAX_CONCURRENT - sem._value})")
        time.sleep(1)   # simula el tiempo de escaneo
    # Al salir del 'with', el semáforo se libera y otro hilo puede entrar

hosts = [f"10.0.0.{i}" for i in range(1, 11)]
threads = [threading.Thread(target=limited_scan, args=(h,)) for h in hosts]
for t in threads: t.start()
for t in threads: t.join()
```

### `threading.Event`: Comunicación entre Hilos

`Event` permite que un hilo señalice a otros que ha ocurrido algo. Es el mecanismo más simple de comunicación entre hilos: un hilo llama a `set()` para activar la señal, y otros hilos pueden esperar con `wait()` hasta que se active, o verificar el estado con `is_set()`.

```python
import threading
import time

stop_event = threading.Event()   # señal de parada compartida

def continuous_scanner(stop_signal):
    """Escanea continuamente hasta que se activa la señal de parada."""
    cycle = 0
    while not stop_signal.is_set():
        cycle += 1
        print(f"  [Scanner] Ciclo de escaneo #{cycle}")
        # wait() con timeout: permite verificar la señal periódicamente
        stop_signal.wait(timeout=1.5)
    print("  [Scanner] Señal de parada recibida, finalizando limpiamente")

scanner_thread = threading.Thread(target=continuous_scanner, args=(stop_event,), daemon=True)
scanner_thread.start()

time.sleep(4)
print("  [Principal] Enviando señal de parada...")
stop_event.set()   # activa la señal: el scanner terminará en su próxima verificación

scanner_thread.join(timeout=3)
print("  [Principal] Scanner detenido")
```

### `threading.Timer`: Ejecución Diferida

`Timer` es una subclase de `Thread` que ejecuta una función después de un retraso especificado. Resulta útil para implementar timeouts de sesión, operaciones programadas, o acciones de limpieza diferidas.

```python
import threading

def session_timeout(session_id):
    """Se ejecuta cuando la sesión expira."""
    print(f"  [!] Sesión {session_id} expirada por inactividad — cerrando conexión")

# Iniciar un timer que se disparará en 5 segundos
timer = threading.Timer(interval=5.0, function=session_timeout, args=("sess_001",))
timer.start()

# Si el usuario realiza alguna acción antes de que expire, cancelar el timer
# timer.cancel()   # esto cancelaría el timer antes de que se ejecute

print("  [*] Timer de sesión iniciado (5 segundos)")
```

### `concurrent.futures.ThreadPoolExecutor`: Pool de Hilos de Alto Nivel

`ThreadPoolExecutor` es la forma moderna y recomendada de gestionar pools de hilos en Python. En lugar de crear y gestionar hilos manualmente, se submiten tareas al pool y este se encarga de asignarlas a los hilos disponibles, reutilizando hilos en lugar de crear uno nuevo por cada tarea.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def check_port(host, port):
    """Simula la verificación de un puerto."""
    time.sleep(0.1)   # simula latencia de red
    # En la práctica: usar socket para intentar conexión
    return host, port, port % 2 == 0   # simula: puertos pares = abiertos

targets = [(f"192.168.1.{i}", p) for i in range(1, 4) for p in [22, 80, 443]]

# max_workers controla la cantidad máxima de hilos simultáneos
with ThreadPoolExecutor(max_workers=5) as executor:
    # submit() envía una tarea y devuelve un objeto Future
    futures = {
        executor.submit(check_port, host, port): (host, port)
        for host, port in targets
    }

    # as_completed() itera sobre los futures a medida que van terminando
    print("  Resultados (en orden de finalización):")
    for future in as_completed(futures):
        host, port, is_open = future.result()
        status = "ABIERTO" if is_open else "cerrado"
        print(f"    {host}:{port} → {status}")
```

---

## La Biblioteca `multiprocessing`

### ¿Cuándo Usar `multiprocessing` en Lugar de `threading`?

`multiprocessing` crea **procesos separados**, cada uno con su propio espacio de memoria e intérprete de Python. Al tener intérpretes independientes, no están sujetos al GIL, lo que permite el **paralelismo real a nivel de CPU**: múltiples procesos pueden ejecutar código Python simultáneamente en distintos núcleos del procesador. El precio de este paralelismo real es el mayor costo de creación de procesos (mayor que la creación de hilos) y la necesidad de mecanismos explícitos de comunicación entre procesos (IPC), dado que no comparten memoria.

En ciberseguridad, `multiprocessing` resulta apropiado para tareas como calcular hashes de millones de contraseñas (CPU-bound puro), análisis estadístico de grandes volúmenes de capturas de red, o procesamiento criptográfico intensivo, donde `threading` no proporcionaría beneficio de rendimiento debido al GIL.

```python
import multiprocessing
import time
import hashlib

def compute_hashes(word_chunk, result_queue):
    """Calcula hashes SHA-256 de una lista de contraseñas (operación CPU-bound)."""
    local_results = []
    for word in word_chunk:
        hash_val = hashlib.sha256(word.encode()).hexdigest()
        local_results.append((word, hash_val))
    result_queue.put(local_results)

# Lista de palabras a hashear
wordlist = [f"password{i}" for i in range(10000)]

# Dividir el trabajo en chunks para cada proceso
num_cores = multiprocessing.cpu_count()
chunk_size = len(wordlist) // num_cores
chunks = [wordlist[i:i + chunk_size] for i in range(0, len(wordlist), chunk_size)]

print(f"  Núcleos disponibles: {num_cores}")
print(f"  Palabras por chunk : {chunk_size}")

result_queue = multiprocessing.Queue()
processes = []

start = time.perf_counter()
for chunk in chunks:
    p = multiprocessing.Process(target=compute_hashes, args=(chunk, result_queue))
    processes.append(p)
    p.start()

for p in processes:
    p.join()

# Recoger los resultados de la queue
all_results = []
while not result_queue.empty():
    all_results.extend(result_queue.get())

elapsed = time.perf_counter() - start
print(f"  Total hashes calculados: {len(all_results):,}")
print(f"  Tiempo con {num_cores} procesos: {elapsed:.3f}s")
```

### Comunicación entre Procesos: `Queue` y `Pipe`

Dado que cada proceso tiene su propio espacio de memoria, compartir datos requiere mecanismos explícitos de comunicación entre procesos (_IPC — Inter-Process Communication_). `multiprocessing` ofrece dos opciones principales:

**`multiprocessing.Queue`**: una cola thread-safe y process-safe que permite que múltiples procesos pongan y saquen elementos. Es la forma más común de recoger resultados de procesos trabajadores.

**`multiprocessing.Pipe`**: un canal bidireccional entre exactamente dos procesos, más eficiente que `Queue` para comunicación directa punto a punto.

```python
import multiprocessing

def worker_with_queue(task_queue, result_queue, worker_id):
    """Procesa tareas de la cola de entrada y pone resultados en la cola de salida."""
    while True:
        task = task_queue.get()
        if task is None:   # None actúa como señal de parada (sentinel value)
            break
        result = f"Worker {worker_id} procesó: {task}"
        result_queue.put(result)

task_q   = multiprocessing.Queue()
result_q = multiprocessing.Queue()

NUM_WORKERS = 3
workers = [
    multiprocessing.Process(target=worker_with_queue, args=(task_q, result_q, i))
    for i in range(NUM_WORKERS)
]
for w in workers: w.start()

# Enviar tareas a la cola
tasks = [f"host_{i}" for i in range(10)]
for task in tasks:
    task_q.put(task)

# Señal de parada: un None por cada worker
for _ in range(NUM_WORKERS):
    task_q.put(None)

for w in workers: w.join()

# Recoger resultados
print("  Resultados procesados:")
while not result_q.empty():
    print(f"    {result_q.get()}")
```

### `multiprocessing.Pool`: Pool de Procesos de Alto Nivel

`multiprocessing.Pool` proporciona una interfaz de alto nivel para distribuir trabajo entre múltiples procesos, similar a `ThreadPoolExecutor` pero con procesos reales en lugar de hilos.

```python
import multiprocessing
import hashlib

def hash_password(password):
    """Función que cada proceso ejecutará sobre su subconjunto de contraseñas."""
    md5    = hashlib.md5(password.encode()).hexdigest()
    sha256 = hashlib.sha256(password.encode()).hexdigest()
    return {"password": password, "md5": md5, "sha256": sha256}

passwords = [f"pass{i:04d}" for i in range(20)]

# Pool.map() distribuye la lista entre los procesos y recoge los resultados en orden
with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
    # map(): bloquea hasta que todos los resultados están listos
    results = pool.map(hash_password, passwords)

    # imap(): iterator perezoso, útil para listas grandes
    # results_iter = pool.imap(hash_password, passwords, chunksize=5)

print(f"  Hashes calculados: {len(results)}")
for r in results[:3]:   # mostrar los primeros 3
    print(f"    {r['password']}: MD5={r['md5'][:8]}... SHA256={r['sha256'][:8]}...")
```

### Variables Compartidas: `Value` y `Array`

Para compartir datos simples entre procesos sin usar una `Queue`, `multiprocessing` ofrece `Value` (para un único valor) y `Array` (para una secuencia de valores del mismo tipo), ambos respaldados por memoria compartida.

```python
import multiprocessing

def increment_counter(shared_counter, lock):
    """Incrementa un contador compartido de forma segura entre procesos."""
    for _ in range(1000):
        with lock:
            shared_counter.value += 1

# Value('i', 0) → entero ('i') inicializado en 0, en memoria compartida
counter = multiprocessing.Value("i", 0)
lock    = multiprocessing.Lock()   # multiprocessing tiene su propio Lock

processes = [
    multiprocessing.Process(target=increment_counter, args=(counter, lock))
    for _ in range(4)
]
for p in processes: p.start()
for p in processes: p.join()

print(f"  Contador final (esperado 4000): {counter.value}")
```

---

## Comparativa Práctica: `threading` vs `multiprocessing`

### I/O-bound: `threading` Gana

```python
import threading
import multiprocessing
import time
import urllib.request

def fetch_url(url):
    """Descarga una URL (operación I/O-bound: CPU espera respuesta de red)."""
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return len(response.read())
    except Exception:
        return 0

urls = ["https://httpbin.org/get"] * 8

# Con threading: el GIL se libera durante la espera de red → concurrencia real
start = time.perf_counter()
threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
for t in threads: t.start()
for t in threads: t.join()
threading_time = time.perf_counter() - start

# Con multiprocessing: funciona también pero con mayor overhead de creación de procesos
start = time.perf_counter()
with multiprocessing.Pool(processes=4) as pool:
    pool.map(fetch_url, urls)
multiprocessing_time = time.perf_counter() - start

print(f"  I/O-bound — threading      : {threading_time:.3f}s")
print(f"  I/O-bound — multiprocessing: {multiprocessing_time:.3f}s")
print(f"  → Para I/O-bound, threading es más rápido (menor overhead)")
```

### CPU-bound: `multiprocessing` Gana

```python
import threading
import multiprocessing
import time
import hashlib

def heavy_cpu_task(n):
    """Tarea intensiva en CPU: calcular muchos hashes."""
    for i in range(100_000):
        hashlib.sha256(f"{n}{i}".encode()).hexdigest()

tasks = list(range(4))

# Con threading: el GIL limita el paralelismo real → no hay mejora
start = time.perf_counter()
threads = [threading.Thread(target=heavy_cpu_task, args=(n,)) for n in tasks]
for t in threads: t.start()
for t in threads: t.join()
threading_time = time.perf_counter() - start

# Con multiprocessing: cada proceso usa un núcleo real → paralelismo genuino
start = time.perf_counter()
with multiprocessing.Pool(processes=4) as pool:
    pool.map(heavy_cpu_task, tasks)
multiprocessing_time = time.perf_counter() - start

print(f"  CPU-bound — threading      : {threading_time:.3f}s")
print(f"  CPU-bound — multiprocessing: {multiprocessing_time:.3f}s")
print(f"  → Para CPU-bound, multiprocessing es más rápido (paralelismo real)")
```

---

## Tabla de Decisión: ¿Qué Usar y Cuándo?

| Criterio                  | `threading`                          | `multiprocessing`                        | `concurrent.futures` |
| ------------------------- | ------------------------------------ | ---------------------------------------- | -------------------- |
| Tipo de tarea             | I/O-bound                            | CPU-bound                                | Ambas                |
| GIL                       | Afectado                             | No afectado                              | Depende del executor |
| Memoria compartida        | Sí (directa)                         | No (IPC necesario)                       | Depende              |
| Overhead de creación      | Bajo                                 | Alto                                     | Medio                |
| Comunicación entre tareas | Sencilla (`Lock`, `Event`)           | Compleja (`Queue`, `Pipe`)               | Abstracta (`Future`) |
| Caso típico en seg.       | Escaneo de puertos, HTTP concurrente | Cracking de hashes, análisis de capturas | Scanner genérico     |

## Buenas Prácticas

Siempre establecer `daemon=True` en hilos de background que no deben bloquear la finalización del programa. Proteger siempre las estructuras de datos compartidas entre hilos con un `Lock`, especialmente listas, diccionarios y contadores, ya que ninguna de estas estructuras es thread-safe en CPython ante acceso concurrente de modificación (aunque las operaciones individuales de lectura sobre tipos inmutables sí lo son). Limitar siempre el número máximo de hilos o procesos simultáneos mediante un `Semaphore` o el parámetro `max_workers` de `ThreadPoolExecutor`, ya que crear un hilo por conexión sin límite puede agotar los recursos del sistema bajo alta carga.

Para `multiprocessing`, recordar siempre encerrar el código de creación de procesos dentro de `if __name__ == "__main__"`, ya que en Windows (y en algunos contextos de Linux con _spawn start method_) los módulos se reimportan en cada proceso hijo, y sin esta protección se produciría un bucle infinito de creación de procesos. Finalmente, preferir `ThreadPoolExecutor` y `Pool` sobre la gestión manual de hilos y procesos cuando sea posible, ya que ambos abstraen la creación, el reciclado y la destrucción de workers, son más fáciles de mantener, y proporcionan el objeto `Future` que simplifica considerablemente la recolección de resultados.
