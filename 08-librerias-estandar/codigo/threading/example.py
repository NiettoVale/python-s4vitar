#!/usr/bin/env python3
import hashlib
import multiprocessing
import threading
import time


def separator(title):
    print(f"\n{'═' * 55}")
    print(f" {title}")
    print(f"{'═' * 55}")


# ═════════════════════════════════════════════════════════════
# TAREA I/O-BOUND: simula una operación que espera (ej: red, disco)
# ═════════════════════════════════════════════════════════════


def task(task_num):
    """Versión base: simplemente espera, sin usar concurrencia."""
    print(f"\n[+] Tarea {task_num} iniciando...")
    time.sleep(2)  # time.sleep() libera el GIL: simula I/O (espera de red, disco, etc.)
    print(f"[+] Tarea {task_num} finalizando...")


def threaded_task(task_num):
    """Misma lógica, mensajes adaptados para identificar que corre en un hilo."""
    print(f"\n[+] Hilo {task_num} iniciando...")
    time.sleep(2)
    print(f"[+] Hilo {task_num} finalizando...")


def process_task(task_num):
    """Misma lógica, mensajes adaptados para identificar que corre en un proceso."""
    print(f"\n[+] Proceso {task_num} iniciando...")
    time.sleep(2)
    print(f"[+] Proceso {task_num} finalizando...")


# ═════════════════════════════════════════════════════════════
# TAREA CPU-BOUND: cálculo intensivo, sin esperas de E/S
# Útil para mostrar el efecto del GIL en una tarea que SÍ usa CPU
# ═════════════════════════════════════════════════════════════


def cpu_intensive_task(task_num, iterations=300_000):
    """Calcula muchos hashes SHA-256: trabajo real de CPU, sin esperas."""
    print(f"\n[+] Tarea CPU {task_num} iniciando ({iterations:,} hashes)...")
    for i in range(iterations):
        hashlib.sha256(f"{task_num}{i}".encode()).hexdigest()
    print(f"[+] Tarea CPU {task_num} finalizando...")


def main():

    # ─────────────────────────────────────────────────────────
    # 1. EJECUCIÓN SECUENCIAL (sin concurrencia)
    # ─────────────────────────────────────────────────────────
    separator("1. EJECUCIÓN SECUENCIAL (sin hilos ni procesos)")

    start = time.perf_counter()
    task(1)
    task(2)
    elapsed_sequential = time.perf_counter() - start

    print(f"\n[*] Tiempo total (secuencial): {elapsed_sequential:.2f}s")
    print("    Las tareas se ejecutan una después de la otra → ~4s en total")

    # ─────────────────────────────────────────────────────────
    # 2. EJECUCIÓN CON THREADING
    # ─────────────────────────────────────────────────────────
    separator("2. EJECUCIÓN CON THREADING")

    start = time.perf_counter()

    # Cada hilo ejecuta threaded_task() de forma independiente.
    # args debe ser una tupla, incluso con un solo argumento: (1,) no (1)
    thread1 = threading.Thread(target=threaded_task, args=(1,))
    thread2 = threading.Thread(target=threaded_task, args=(2,))

    # start() lanza el hilo; no bloquea, la ejecución continúa de inmediato
    thread1.start()
    thread2.start()

    # join() bloquea hasta que el hilo correspondiente termine.
    # Sin estos join(), el script podría terminar antes de que los hilos acaben.
    thread1.join()
    thread2.join()

    elapsed_threading = time.perf_counter() - start

    print("\n[+] Los hilos finalizaron correctamente.")
    print(f"[*] Tiempo total (threading): {elapsed_threading:.2f}s")
    print("    Ambos time.sleep() ocurren en paralelo → ~2s en total")
    print("    (time.sleep() libera el GIL, por eso threading SÍ acelera esta tarea)")

    # ─────────────────────────────────────────────────────────
    # 3. EJECUCIÓN CON MULTIPROCESSING
    # ─────────────────────────────────────────────────────────
    separator("3. EJECUCIÓN CON MULTIPROCESSING")

    start = time.perf_counter()

    # La sintaxis es prácticamente idéntica a threading.Thread,
    # pero Process crea un PROCESO del sistema operativo completo,
    # con su propio espacio de memoria e intérprete de Python.
    process1 = multiprocessing.Process(target=process_task, args=(1,))
    process2 = multiprocessing.Process(target=process_task, args=(2,))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    elapsed_multiprocessing = time.perf_counter() - start

    print("\n[+] Los procesos finalizaron correctamente.")
    print(f"[*] Tiempo total (multiprocessing): {elapsed_multiprocessing:.2f}s")
    print("    También ~2s, pero con mayor overhead de creación de procesos")

    # ─────────────────────────────────────────────────────────
    # 4. RESUMEN COMPARATIVO (tarea I/O-bound)
    # ─────────────────────────────────────────────────────────
    separator("4. RESUMEN — TAREA I/O-BOUND (time.sleep)")

    print(f"  {'MODELO':<20}{'TIEMPO':<12}{'OBSERVACIÓN'}")
    print(f"  {'-'*20}{'-'*12}{'-'*30}")
    print(
        f"  {'Secuencial':<20}{elapsed_sequential:.2f}s{'':<6}Sin concurrencia, suma de tiempos"
    )
    print(
        f"  {'Threading':<20}{elapsed_threading:.2f}s{'':<6}I/O-bound → threading es ideal"
    )
    print(
        f"  {'Multiprocessing':<20}{elapsed_multiprocessing:.2f}s{'':<6}Funciona, pero con más overhead"
    )

    # ─────────────────────────────────────────────────────────
    # 5. COMPARATIVA CON TAREA CPU-BOUND
    # Aquí se ve el efecto REAL del GIL: threading no ayuda en absoluto
    # ─────────────────────────────────────────────────────────
    separator("5. COMPARATIVA CON TAREA CPU-BOUND (hashing)")

    print("[*] Ejecutando la misma carga de trabajo con threading y multiprocessing...")
    print("    (cálculo de hashes SHA-256: trabajo real de CPU, sin esperas)\n")

    # --- threading con tarea CPU-bound ---
    start = time.perf_counter()
    cpu_thread1 = threading.Thread(target=cpu_intensive_task, args=(1,))
    cpu_thread2 = threading.Thread(target=cpu_intensive_task, args=(2,))
    cpu_thread1.start()
    cpu_thread2.start()
    cpu_thread1.join()
    cpu_thread2.join()
    elapsed_cpu_threading = time.perf_counter() - start

    # --- multiprocessing con tarea CPU-bound ---
    start = time.perf_counter()
    cpu_process1 = multiprocessing.Process(target=cpu_intensive_task, args=(1,))
    cpu_process2 = multiprocessing.Process(target=cpu_intensive_task, args=(2,))
    cpu_process1.start()
    cpu_process2.start()
    cpu_process1.join()
    cpu_process2.join()
    elapsed_cpu_multiprocessing = time.perf_counter() - start

    print(f"\n  {'MODELO':<20}{'TIEMPO':<12}{'OBSERVACIÓN'}")
    print(f"  {'-'*20}{'-'*12}{'-'*40}")
    print(
        f"  {'Threading':<20}{elapsed_cpu_threading:.2f}s{'':<6}GIL limita el paralelismo real"
    )
    print(
        f"  {'Multiprocessing':<20}{elapsed_cpu_multiprocessing:.2f}s{'':<6}Paralelismo real entre núcleos"
    )

    if elapsed_cpu_multiprocessing < elapsed_cpu_threading:
        improvement = (1 - elapsed_cpu_multiprocessing / elapsed_cpu_threading) * 100
        print(
            f"\n  → multiprocessing fue ~{improvement:.0f}% más rápido en esta tarea CPU-bound"
        )
    else:
        print(
            "\n  → En este entorno la diferencia no fue significativa "
            "(depende del número de núcleos disponibles)"
        )


# IMPORTANTE: en multiprocessing, todo el código que crea procesos debe
# estar dentro de este bloque. Sin esto, en Windows (y en algunos casos
# de Linux con 'spawn') se produciría un bucle infinito de recreación
# de procesos, ya que el módulo se reimporta en cada proceso hijo.
if __name__ == "__main__":
    main()
