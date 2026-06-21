#!/usr/bin/env python3
from collections import deque
import copy

ANCHO = 70


def titulo(texto):
    print("\n" + "═" * ANCHO)
    print(f" {texto}")
    print("═" * ANCHO)


def subtitulo(texto):
    print(f"\n── {texto} {'─' * (ANCHO - len(texto) - 4)}")


# ---------------------------------------------------------------------------
# 1. Datos heterogéneos + slicing: top hallazgos de una auditoría
# ---------------------------------------------------------------------------
titulo("1. Slicing aplicado a un listado de hallazgos")

# Cada hallazgo: [CVE, host, puntaje_CVSS]
hallazgos = [
    ["CVE-2021-41773", "192.168.1.10", 9.8],
    ["CVE-2022-26134", "192.168.1.11", 9.1],
    ["CVE-2023-23397", "192.168.1.12", 8.8],
    ["CVE-2019-0708",  "192.168.1.13", 7.5],
    ["CVE-2020-1472",  "192.168.1.14", 10.0],
    ["CVE-2017-0144",  "192.168.1.15", 8.1],
]

# Ordenar por puntaje CVSS de mayor a menor (sorted -> no modifica la lista original)
hallazgos_ordenados = sorted(hallazgos, key=lambda h: h[2], reverse=True)

# Slicing: quedarnos solo con el top 3 de mayor severidad
top_3 = hallazgos_ordenados[:3]

subtitulo("Top 3 hallazgos críticos (por CVSS)")
for cve, host, cvss in top_3:
    print(f"  {cve:<18}{host:<16}CVSS {cvss:>4.1f}")


# ---------------------------------------------------------------------------
# 2. Matriz / lista anidada: mapa de calor de riesgo por categoría
# ---------------------------------------------------------------------------
titulo("2. Matriz de riesgo (lista de listas)")

categorias = ["Web", "AD", "Red"]
hosts_matriz = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]

# Cada fila representa un host, cada columna una categoría (0=bajo, 1=medio, 2=alto)
matriz_riesgo = [
    [2, 0, 1],
    [1, 2, 0],
    [0, 1, 2],
]

simbolos = {0: "·", 1: "▲", 2: "■"}

subtitulo("Mapa de riesgo por host / categoría")
encabezado = "  " + "".join(f"{c:^6}" for c in categorias)
print(encabezado)
for host, fila in zip(hosts_matriz, matriz_riesgo):
    celdas = "".join(f"{simbolos[valor]:^6}" for valor in fila)
    print(f"  {celdas}   {host}")
print("\n  Referencia: · bajo   ▲ medio   ■ alto")


# ---------------------------------------------------------------------------
# 3. Referencias vs. copias: snapshot de sesiones activas
# ---------------------------------------------------------------------------
titulo("3. Aliasing vs. copia independiente")

sesiones_activas = ["sess_001", "sess_002", "sess_003"]

# Aliasing: 'referencia' apunta a la MISMA lista en memoria
referencia = sesiones_activas
referencia.append("sess_004")

# copy(): snapshot independiente para un reporte, no se ve afectado por cambios futuros
snapshot_reporte = sesiones_activas.copy()
sesiones_activas.append("sess_005")   # esto NO debe aparecer en el snapshot ya tomado

subtitulo("Resultado")
print(f"  Sesiones activas (en vivo): {sesiones_activas}")
print(f"  Snapshot para el reporte:   {snapshot_reporte}")
print("  -> El snapshot quedó congelado en el momento exacto en que se copió.")


# ---------------------------------------------------------------------------
# 4. append / insert / pop / remove: ciclo de vida de una cola de tareas
# ---------------------------------------------------------------------------
titulo("4. Ciclo de vida de una cola de tareas de escaneo")

tareas = []
tareas.append("escaneo_puertos")
tareas.append("enumeracion_servicios")
tareas.insert(0, "resolucion_dns")   # se agrega con prioridad, al inicio

subtitulo("Cola inicial")
print(f"  {tareas}")

tarea_en_curso = tareas.pop(0)
print(f"\n  Procesando: '{tarea_en_curso}'")

tareas.remove("enumeracion_servicios")   # se cancela esa tarea puntual
print(f"  Cola tras cancelar una tarea: {tareas}")


# ---------------------------------------------------------------------------
# 5. DFS con una pila: cadena de escalada de privilegios
# ---------------------------------------------------------------------------
titulo("5. DFS: explorando una cadena de escalada de privilegios")

# Grafo simulado de rutas de escalada: usuario -> [siguientes pasos posibles]
grafo_escalada = {
    "www-data":        ["service_backup", "service_cron"],
    "service_backup":  ["root (via SUID)"],
    "service_cron":    ["root (via writable cronjob)"],
}

pila = ["www-data"]
ruta_explorada = []

while pila:
    usuario_actual = pila.pop()
    if usuario_actual in ruta_explorada:
        continue
    ruta_explorada.append(usuario_actual)

    siguientes_pasos = grafo_escalada.get(usuario_actual, [])
    for paso in siguientes_pasos:
        pila.append(paso)

subtitulo("Orden de exploración (profundidad primero)")
for nivel, paso in enumerate(ruta_explorada):
    print(f"  {'  ' * nivel}└─ {paso}")


# ---------------------------------------------------------------------------
# 6. BFS con deque: propagación simulada de un worm por capas de cercanía
# ---------------------------------------------------------------------------
titulo("6. BFS: propagación de un worm por capas de cercanía")

topologia_red = {
    "192.168.1.10": ["192.168.1.20", "192.168.1.21"],
    "192.168.1.20": ["192.168.1.30"],
    "192.168.1.21": ["192.168.1.31", "192.168.1.32"],
}

cola_propagacion = deque([("192.168.1.10", 0)])   # (host, capa de distancia)
infectados = set()

subtitulo("Hosts comprometidos por capa")
while cola_propagacion:
    host_actual, capa = cola_propagacion.popleft()
    if host_actual in infectados:
        continue
    infectados.add(host_actual)
    print(f"  Capa {capa}: {host_actual}")

    for vecino in topologia_red.get(host_actual, []):
        cola_propagacion.append((vecino, capa + 1))

print(f"\n  Total de hosts comprometidos: {len(infectados)}")
# ---------------------------------------------------------------------------
# 7. extend(): fusionar listas de IOCs provenientes de distintos feeds
# ---------------------------------------------------------------------------
titulo("7. extend(): fusión de indicadores de compromiso (IOCs)")

iocs_feed_a = ["185.220.101.5", "45.137.21.9"]
iocs_feed_b = ["185.220.101.5", "194.165.16.3", "91.243.85.17"]

iocs_consolidados = []
iocs_consolidados.extend(iocs_feed_a)
iocs_consolidados.extend(iocs_feed_b)

subtitulo("Antes y después de deduplicar")
print(f"  Consolidado (con duplicados): {iocs_consolidados}")

# dict.fromkeys() conserva el orden de aparición y elimina duplicados
iocs_unicos = list(dict.fromkeys(iocs_consolidados))
print(f"  Consolidado (sin duplicados): {iocs_unicos}")


# ---------------------------------------------------------------------------
# 8. sort() in-place: ordenar una línea de tiempo de intentos fallidos
# ---------------------------------------------------------------------------
titulo("8. sort() in-place: cronología de intentos de login fallidos")

# Cada evento: [timestamp_unix, usuario, ip_origen]
intentos_fallidos = [
    [1718812980, "admin",   "203.0.113.5"],
    [1718812920, "backup",  "198.51.100.7"],
    [1718813040, "admin",   "203.0.113.5"],
    [1718812955, "root",    "203.0.113.9"],
]

intentos_fallidos.sort(key=lambda evento: evento[0])   # modifica la lista original

subtitulo("Eventos ordenados cronológicamente")
for ts, usuario, ip in intentos_fallidos:
    print(f"  [{ts}]  usuario={usuario:<8} origen={ip}")


# ---------------------------------------------------------------------------
# 9. [::-1]: reconstruir el orden inverso de una cadena de custodia
# ---------------------------------------------------------------------------
titulo("9. Slicing inverso: cadena de custodia de un incidente")

pasos_respuesta_incidente = [
    "1. Detección de alerta en el SIEM",
    "2. Aislamiento del host afectado",
    "3. Captura de memoria (memory dump)",
    "4. Análisis forense del binario",
    "5. Erradicación y limpieza",
]

subtitulo("Orden cronológico original")
for paso in pasos_respuesta_incidente:
    print(f"  {paso}")

subtitulo("Orden inverso (para revisión retrospectiva, del cierre al inicio)")
for paso in pasos_respuesta_incidente[::-1]:
    print(f"  {paso}")


# ---------------------------------------------------------------------------
# 10. clear() / del: purga de credenciales temporales tras un engagement
# ---------------------------------------------------------------------------
titulo("10. clear() y del: purga de credenciales en memoria")

cache_credenciales = ["admin:S3cr3t!", "svc_backup:Backup2024", "guest:guest"]

subtitulo("Antes de la purga")
print(f"  {cache_credenciales}")

del cache_credenciales[1]        # se elimina una credencial puntual por índice
print(f"\n  Tras eliminar una credencial puntual: {cache_credenciales}")

cache_credenciales.clear()       # al finalizar el engagement, se purga todo el caché
print(f"  Caché purgado al finalizar el engagement: {cache_credenciales}")


# ---------------------------------------------------------------------------
# 11. Comprensión de listas: generar reglas de firewall a partir de IOCs
# ---------------------------------------------------------------------------
titulo("11. Comprensión de listas: generación de reglas de firewall")

ips_a_bloquear = ["185.220.101.5", "194.165.16.3", "91.243.85.17"]

reglas_firewall = [f"iptables -A INPUT -s {ip} -j DROP" for ip in ips_a_bloquear]

subtitulo("Reglas generadas")
for regla in reglas_firewall:
    print(f"  {regla}")


# ---------------------------------------------------------------------------
# 12. Copia profunda: ramificar un árbol de escenarios de ataque
# ---------------------------------------------------------------------------
titulo("12. copy.deepcopy(): ramificar un escenario de ataque simulado")

# Árbol de decisión: cada nodo tiene una lista de posibles próximos pasos
escenario_base = {
    "punto_entrada": "phishing",
    "siguientes_pasos": ["movimiento_lateral", "persistencia"],
}

# Se necesita una rama alternativa SIN afectar el escenario base original
escenario_alternativo = copy.deepcopy(escenario_base)
escenario_alternativo["punto_entrada"] = "exploit_web"
escenario_alternativo["siguientes_pasos"].append("exfiltracion")

subtitulo("Comparación de escenarios")
print(f"  Escenario base:        {escenario_base}")
print(f"  Escenario alternativo: {escenario_alternativo}")
print("  -> Modificar la rama alternativa no alteró el escenario base original.")