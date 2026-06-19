#!/usr/bin/env python3

# ---------------------------------------------------------------------------
# 1. Sintaxis básica de funciones lambda
# ---------------------------------------------------------------------------
print("== 1. Sintaxis básica ==")

saludo = lambda: "¡Hola Mundo!"
print(saludo())

cuadrado = lambda numero: numero ** 2
print(f"Cuadrado de 2: {cuadrado(2)}")

suma = lambda x, y: x + y
print(f"Suma de 7 y 3: {suma(7, 3)}")


# ---------------------------------------------------------------------------
# 2. Lambda + map(): transformar cada elemento de una lista
# ---------------------------------------------------------------------------
print("\n== 2. Lambda + map() ==")

puertos = [21, 22, 23, 80, 443, 445, 3389]

# Convertir cada puerto a su representación en string con formato "puerto/tcp"
puertos_formateados = list(map(lambda p: f"{p}/tcp", puertos))
print(f"Puertos formateados: {puertos_formateados}")

cuadrados = list(map(lambda x: x ** 2, puertos))
print(f"Cuadrados (ejemplo ilustrativo): {cuadrados}")


# ---------------------------------------------------------------------------
# 3. Lambda + filter(): conservar solo los elementos que cumplen una condición
# ---------------------------------------------------------------------------
print("\n== 3. Lambda + filter() ==")

pares = list(filter(lambda x: x % 2 == 0, puertos))
print(f"Puertos pares: {pares}")

puertos_criticos = [21, 23, 445, 3389]
hallazgos_criticos = list(filter(lambda p: p in puertos_criticos, puertos))
print(f"Hallazgos críticos: {hallazgos_criticos}")

# Filtrar hosts activos a partir de una lista de diccionarios
resultados_escaneo = [
    {"host": "192.168.1.10", "activo": True},
    {"host": "192.168.1.11", "activo": False},
    {"host": "192.168.1.12", "activo": True},
]
hosts_activos = list(filter(lambda r: r["activo"], resultados_escaneo))
print(f"Hosts activos: {[h['host'] for h in hosts_activos]}")


# ---------------------------------------------------------------------------
# 4. Lambda + sorted(): definir un criterio de ordenamiento personalizado
# ---------------------------------------------------------------------------
print("\n== 4. Lambda + sorted() ==")

hallazgos = [
    {"host": "192.168.1.10", "puerto": 22, "severidad": 7},
    {"host": "192.168.1.11", "puerto": 21, "severidad": 9},
    {"host": "192.168.1.12", "puerto": 80, "severidad": 4},
]

# Ordenar de mayor a menor severidad
hallazgos_ordenados = sorted(hallazgos, key=lambda h: h["severidad"], reverse=True)

print("Hallazgos ordenados por severidad (descendente):")
for hallazgo in hallazgos_ordenados:
    print(f"  -> {hallazgo['host']}:{hallazgo['puerto']} (severidad {hallazgo['severidad']})")

# Ordenar una lista simple de hosts según la longitud de su dirección IP
hosts = ["192.168.1.10", "10.0.0.1", "172.16.0.100"]
hosts_por_longitud = sorted(hosts, key=lambda h: len(h))
print(f"Hosts ordenados por longitud de dirección: {hosts_por_longitud}")


# ---------------------------------------------------------------------------
# 5. Comparación: lambda vs. función equivalente con def
# ---------------------------------------------------------------------------
print("\n== 5. Lambda vs. def ==")

def obtener_severidad(hallazgo):
    return hallazgo["severidad"]

hallazgos_ordenados_def = sorted(hallazgos, key=obtener_severidad, reverse=True)
hallazgos_ordenados_lambda = sorted(hallazgos, key=lambda h: h["severidad"], reverse=True)

print(f"Resultado con def:    {[h['host'] for h in hallazgos_ordenados_def]}")
print(f"Resultado con lambda: {[h['host'] for h in hallazgos_ordenados_lambda]}")
print("Ambos producen el mismo resultado; la lambda evita declarar una función aparte.")