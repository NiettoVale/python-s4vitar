#!/usr/bin/env python3
"""
Ejemplos prácticos de diccionarios en Python aplicados a ciberseguridad.

Cubre: orden de inserción, claves únicas, acceso con corchetes vs. get(),
del/pop()/popitem()/clear(), keys()/values()/items() como vistas dinámicas,
setdefault()/defaultdict, combinación de diccionarios (update, |, **),
comprensión de diccionarios, parseo de JSON y diccionarios anidados.

La salida está formateada para leerse cómodamente en una terminal.
"""

import json
from collections import defaultdict


# ---------------------------------------------------------------------------
# Utilidades de presentación
# ---------------------------------------------------------------------------

ANCHO = 70


def titulo(texto):
    print("\n" + "═" * ANCHO)
    print(f" {texto}")
    print("═" * ANCHO)


def subtitulo(texto):
    print(f"\n── {texto} {'─' * (ANCHO - len(texto) - 4)}")


# ---------------------------------------------------------------------------
# 1. Orden de inserción preservado (Python 3.7+)
# ---------------------------------------------------------------------------
titulo("1. Orden de inserción preservado")

reporte = {}
reporte["fecha"] = "2026-06-21"
reporte["analista"] = "fran"
reporte["alcance"] = "192.168.1.0/24"

subtitulo("Iteración (respeta el orden en que se agregaron las claves)")
for clave, valor in reporte.items():
    print(f"  {clave}: {valor}")


# ---------------------------------------------------------------------------
# 2. Claves únicas: el riesgo de sobrescribir sin darse cuenta
# ---------------------------------------------------------------------------
titulo("2. Claves únicas (cuidado con sobrescribir)")

vulnerabilidades_por_host = {}
vulnerabilidades_por_host["192.168.1.10"] = ["CVE-2020-1472"]

subtitulo("Antes de la sobrescritura accidental")
print(f"  {vulnerabilidades_por_host}")

vulnerabilidades_por_host["192.168.1.10"] = ["CVE-2021-41773"]   # pisó el valor anterior

subtitulo("Después (el primer CVE se perdió)")
print(f"  {vulnerabilidades_por_host}")


# ---------------------------------------------------------------------------
# 3. Acceso: corchetes vs. get()
# ---------------------------------------------------------------------------
titulo("3. Acceso con corchetes vs. get()")

config_herramienta = {"timeout": 5, "max_hilos": 10}

subtitulo("get() con valor por defecto (sin riesgo de KeyError)")
proxy = config_herramienta.get("proxy", "no configurado")
print(f"  proxy: {proxy}")

subtitulo("Acceso directo a una clave inexistente (capturado)")
try:
    user_agent = config_herramienta["user_agent"]
except KeyError as error:
    print(f"  Error capturado: clave {error} no definida")


# ---------------------------------------------------------------------------
# 4. del / pop() / popitem() / clear(): ciclo de vida de sesiones
# ---------------------------------------------------------------------------
titulo("4. Eliminación: del, pop(), popitem(), clear()")

tokens_activos = {"tok_aa": "192.168.1.10", "tok_bb": "192.168.1.11", "tok_cc": "192.168.1.12"}

del tokens_activos["tok_aa"]
subtitulo("Tras del")
print(f"  {tokens_activos}")

ip_revocada = tokens_activos.pop("tok_bb")
subtitulo("Tras pop() (devuelve el valor eliminado)")
print(f"  IP del token revocado: {ip_revocada}")
print(f"  Tokens restantes: {tokens_activos}")

token, ip = tokens_activos.popitem()
subtitulo("Tras popitem() (elimina el último insertado)")
print(f"  Eliminado: {token} -> {ip}")

tokens_activos.clear()
subtitulo("Tras clear()")
print(f"  {tokens_activos}")


# ---------------------------------------------------------------------------
# 5. keys() / values() / items() como vistas dinámicas
# ---------------------------------------------------------------------------
titulo("5. Vistas dinámicas: keys(), values(), items()")

servicios = {"ssh": 22, "https": 443}
vista_valores = servicios.values()

subtitulo("Antes de modificar el diccionario")
print(f"  {list(vista_valores)}")

servicios["smb"] = 445   # se agrega DESPUÉS de obtener la vista

subtitulo("Después (la vista reflejó el cambio automáticamente)")
print(f"  {list(vista_valores)}")


# ---------------------------------------------------------------------------
# 6. setdefault() y defaultdict: agrupar hallazgos por categoría
# ---------------------------------------------------------------------------
titulo("6. setdefault() y defaultdict()")

eventos_log = [
    ("autenticacion", "intento fallido desde 203.0.113.5"),
    ("autenticacion", "login exitoso de admin"),
    ("red", "escaneo de puertos detectado"),
]

subtitulo("Con setdefault()")
eventos_por_categoria = {}
for categoria, descripcion in eventos_log:
    eventos_por_categoria.setdefault(categoria, []).append(descripcion)
for categoria, lista in eventos_por_categoria.items():
    print(f"  {categoria}: {lista}")

subtitulo("Con defaultdict (sin necesidad de setdefault)")
eventos_por_categoria_dd = defaultdict(list)
for categoria, descripcion in eventos_log:
    eventos_por_categoria_dd[categoria].append(descripcion)
for categoria, lista in eventos_por_categoria_dd.items():
    print(f"  {categoria}: {lista}")


# ---------------------------------------------------------------------------
# 7. Combinar diccionarios: update(), | y **
# ---------------------------------------------------------------------------
titulo("7. Combinar diccionarios")

perfil_por_defecto = {"nivel_log": "info", "modo": "pasivo"}
perfil_agresivo = {"modo": "activo", "hilos": 50}

subtitulo("update() (modifica el original)")
copia_para_update = perfil_por_defecto.copy()
copia_para_update.update(perfil_agresivo)
print(f"  {copia_para_update}")

subtitulo("Operador | (genera uno nuevo, no modifica los originales)")
perfil_final = perfil_por_defecto | perfil_agresivo
print(f"  {perfil_final}")
print(f"  Original sin cambios: {perfil_por_defecto}")


# ---------------------------------------------------------------------------
# 8. Comprensión de diccionarios
# ---------------------------------------------------------------------------
titulo("8. Comprensión de diccionarios")

hallazgos_cvss = {"CVE-2020-1472": 10.0, "CVE-2021-41773": 9.8, "CVE-2019-0708": 7.5}

subtitulo("Filtrar solo los hallazgos críticos (CVSS >= 9.0)")
criticos = {cve: cvss for cve, cvss in hallazgos_cvss.items() if cvss >= 9.0}
print(f"  {criticos}")

subtitulo("Invertir clave <-> valor")
cvss_a_cve = {cvss: cve for cve, cvss in hallazgos_cvss.items()}
print(f"  {cvss_a_cve}")


# ---------------------------------------------------------------------------
# 9. JSON <-> diccionarios
# ---------------------------------------------------------------------------
titulo("9. Parseo de JSON a diccionario")

respuesta_api = '{"host": "192.168.1.10", "puertos_abiertos": [22, 80, 443], "activo": true}'
datos = json.loads(respuesta_api)

subtitulo("Diccionario resultante")
print(f"  Host: {datos['host']}")
print(f"  Puertos: {datos['puertos_abiertos']}")
print(f"  Activo: {datos['activo']}")


# ---------------------------------------------------------------------------
# 10. Diccionarios anidados: inventario jerárquico de red
# ---------------------------------------------------------------------------
titulo("10. Diccionarios anidados")

inventario = {
    "192.168.1.10": {
        "estado": "activo",
        "servicios": {22: "OpenSSH 8.2", 443: "nginx 1.18"},
    },
    "192.168.1.11": {
        "estado": "activo",
        "servicios": {445: "Samba 4.6"},
    },
}

subtitulo("Recorrido completo del inventario")
for host, info in inventario.items():
    print(f"  {host} ({info['estado']})")
    for puerto, version in info["servicios"].items():
        print(f"    -> {puerto}: {version}")

subtitulo("Acceso defensivo con get() encadenado")
version_puerto_8080 = inventario.get("192.168.1.10", {}).get("servicios", {}).get(8080, "no detectado")
print(f"  Servicio en puerto 8080: {version_puerto_8080}")

