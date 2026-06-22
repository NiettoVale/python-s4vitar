#!/usr/bin/env python3
"""
Ejemplos prácticos de entrada y salida en Python aplicados a ciberseguridad.
Escenarios distintos a los utilizados en las notas teóricas.

Cubre: print() avanzado, colores ANSI, input() con validación, getpass,
formateo de tablas, números en distintas bases, codificación de caracteres,
separación stdout/stderr y construcción de una mini CLI interactiva.
"""

import sys
import getpass
import textwrap

# ═══════════════════════════════════════════════════════════════════════
# PALETA DE COLORES ANSI Y UTILIDADES DE PRESENTACIÓN
# ═══════════════════════════════════════════════════════════════════════

R  = "\033[0m"       # reset
N  = "\033[1m"       # negrita
RO = "\033[91m"      # rojo
VE = "\033[92m"      # verde
AM = "\033[93m"      # amarillo
AZ = "\033[94m"      # azul
MG = "\033[95m"      # magenta
CY = "\033[96m"      # cian

ANCHO = 65


def banner():
    print(f"\n{N}{MG}" + "█" * ANCHO + R)
    print(f"{N}{MG}{'RECON FRAMEWORK - INPUT/OUTPUT DEMO':^{ANCHO}}{R}")
    print(f"{N}{MG}" + "█" * ANCHO + R)


def seccion(texto):
    print(f"\n{N}{AZ}══ {texto} {'═' * (ANCHO - len(texto) - 4)}{R}")


def ok(msg):    print(f"  {VE}[+]{R} {msg}")
def info(msg):  print(f"  {AZ}[*]{R} {msg}")
def warn(msg):  print(f"  {AM}[!]{R} {msg}", file=sys.stderr)
def error(msg): print(f"  {RO}[-]{R} {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════
# 1. print() AVANZADO: sep, end y flush
# ═══════════════════════════════════════════════════════════════════════

banner()
seccion("1. print() avanzado: sep, end y flush")

# sep personalizado: construir una línea de log estructurada
campos = ["2026-06-21 14:32:01", "INFO", "192.168.1.10", "Puerto 443 abierto"]
print("  " + " | ".join(campos))

# end="": construir una barra de progreso simple sin saltos de línea intermedios
import time
print(f"\n  {AZ}[*]{R} Escaneando puertos", end=" ")
for puerto in [22, 80, 443, 445, 3389]:
    print(f"{puerto}", end=" ", flush=True)
    time.sleep(0.08)
print(f"→ {VE}listo{R}")

# Redirigir print() a un archivo en vez de la consola
with open("/tmp/demo_salida.txt", "w") as f:
    print("Reporte generado automáticamente", file=f)
    print("Hallazgo: Puerto 445/SMB abierto en 192.168.1.10", file=f)

with open("/tmp/demo_salida.txt") as f:
    contenido = f.read().strip()
ok(f"Contenido guardado en archivo: '{contenido}'")


# ═══════════════════════════════════════════════════════════════════════
# 2. FORMATEO DE TABLAS CON ALINEACIÓN
# ═══════════════════════════════════════════════════════════════════════

seccion("2. Tablas con alineación de columnas")

credenciales_probadas = [
    ("admin",    "admin123",    "❌ Fallida"),
    ("root",     "toor",        "❌ Fallida"),
    ("backup",   "backup2024",  "✅ Exitosa"),
    ("svc_web",  "P@ssw0rd!",   "❌ Fallida"),
]

print(f"\n  {'USUARIO':<15}{'CONTRASEÑA':<18}{'RESULTADO'}")
print("  " + "─" * 45)
for usuario, clave, resultado in credenciales_probadas:
    color = VE if "Exitosa" in resultado else RO
    print(f"  {usuario:<15}{clave:<18}{color}{resultado}{R}")
print("  " + "─" * 45)
exitosas = sum(1 for _, _, r in credenciales_probadas if "Exitosa" in r)
print(f"  {'Total exitosas:':<30}{VE}{exitosas}/{len(credenciales_probadas)}{R}")


# ═══════════════════════════════════════════════════════════════════════
# 3. FORMATEO DE NÚMEROS: bases, decimales y separadores
# ═══════════════════════════════════════════════════════════════════════

seccion("3. Formateo de números")

# Representación de una MAC address byte a byte
mac_bytes = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]
mac_str = ":".join(f"{b:02x}" for b in mac_bytes)
print(f"\n  MAC address:  {CY}{mac_str.upper()}{R}")

# Representación de flags TCP como bits individuales (SYN, ACK, FIN, RST, PSH, URG)
flags_tcp = 0b00010010   # SYN + ACK
print(f"  Flags TCP:    {CY}{flags_tcp:#010b}{R}  ({flags_tcp:#04x})")
activos = [n for i, n in enumerate(["FIN","SYN","RST","PSH","ACK","URG"]) if flags_tcp & (1 << i)]
print(f"  Flags activos: {', '.join(activos)}")

# Tamaño de archivos en distintas unidades
bytes_captura = 1_874_523_648
kb = bytes_captura / 1024
mb = kb / 1024
gb = mb / 1024
print(f"\n  Tamaño de la captura PCAP:")
print(f"    {bytes_captura:>15,} bytes")
print(f"    {kb:>15,.1f} KB")
print(f"    {mb:>15,.2f} MB")
print(f"    {gb:>15,.3f} GB")


# ═══════════════════════════════════════════════════════════════════════
# 4. CODIFICACIÓN: encode/decode en contexto de red
# ═══════════════════════════════════════════════════════════════════════

seccion("4. Codificación de caracteres")

import base64

# Simular datos recibidos de un servicio HTTP con cabecera Authorization Basic
usuario_raw = "admin"
clave_raw   = "Str0ng#P@ss!"
credencial  = f"{usuario_raw}:{clave_raw}"

# Codificar a Base64 (como lo haría un cliente HTTP)
credencial_b64 = base64.b64encode(credencial.encode("utf-8")).decode("ascii")
print(f"\n  Credencial original : {credencial}")
print(f"  Authorization Basic : Basic {CY}{credencial_b64}{R}")

# Decodificar el header interceptado (como lo haría un proxy o un sniffer)
interceptado = f"Basic {credencial_b64}"
parte_b64 = interceptado.split(" ")[1]
decodificado = base64.b64decode(parte_b64).decode("utf-8")
ok(f"Credencial interceptada y decodificada: {VE}{decodificado}{R}")

# Manejar bytes con caracteres inválidos (respuesta binaria de un servicio)
respuesta_binaria = b"HTTP/1.1 200 OK\r\nServer: Apache\r\n\xff\xfe\x00\r\n"
texto_seguro  = respuesta_binaria.decode("utf-8", errors="replace")
texto_limpio  = respuesta_binaria.decode("utf-8", errors="ignore")
print(f"\n  Con replace : {repr(texto_seguro[:50])}")
print(f"  Con ignore  : {repr(texto_limpio[:50])}")


# ═══════════════════════════════════════════════════════════════════════
# 5. textwrap: formatear descripciones de CVEs
# ═══════════════════════════════════════════════════════════════════════

seccion("5. textwrap: presentación de CVEs")

cves = [
    ("CVE-2021-44228", 10.0, "Log4Shell: ejecución remota de código en Apache Log4j mediante una cadena de lookup JNDI especialmente construida enviada a través de cualquier campo que sea logueado por la aplicación afectada."),
    ("CVE-2019-0708",   9.8, "BlueKeep: vulnerabilidad de ejecución remota de código en los Servicios de Escritorio Remoto (RDS) de Windows que no requiere autenticación previa y puede propagarse de forma similar a un gusano."),
]

for cve_id, cvss, descripcion in cves:
    color_cvss = RO if cvss >= 9.0 else AM
    print(f"\n  {N}{cve_id}{R}  CVSS: {color_cvss}{cvss}{R}")
    lineas = textwrap.wrap(descripcion, width=55)
    for linea in lineas:
        print(f"    {linea}")


# ═══════════════════════════════════════════════════════════════════════
# 6. stdout vs stderr: separar resultados de mensajes de estado
# ═══════════════════════════════════════════════════════════════════════

seccion("6. stdout vs stderr")

info("Los mensajes de estado van a stderr (sys.stderr)")
info("Los resultados van a stdout (sys.stdout)  → redirigibles con >")

hosts_simulados = {
    "192.168.1.10": True,
    "192.168.1.11": False,
    "192.168.1.12": True,
}

for host, activo in hosts_simulados.items():
    if activo:
        # resultado real: va a stdout
        print(f"  {host}")
        ok(f"{host} activo")
    else:
        # advertencia de estado: va a stderr
        warn(f"{host} no respondió")


# ═══════════════════════════════════════════════════════════════════════
# 7. MINI CLI INTERACTIVA con input() + getpass + validación
# ═══════════════════════════════════════════════════════════════════════

seccion("7. Mini CLI interactiva")

MENU = {
    "1": "Escanear un host",
    "2": "Autenticarse en el framework",
    "3": "Salir",
}


def mostrar_menu():
    print(f"\n  {N}Menú principal:{R}")
    for clave, opcion in MENU.items():
        print(f"    {CY}[{clave}]{R} {opcion}")


def pedir_opcion():
    """Solicita una opción del menú y la valida antes de devolverla."""
    while True:
        opcion = input(f"\n  Opción {AZ}[1-{len(MENU)}]{R}: ").strip()
        if opcion in MENU:
            return opcion
        error(f"Opción '{opcion}' no válida. Elegí entre {list(MENU.keys())}.")


def flujo_escaneo():
    """Solicita una IP y un número de puerto con validación integrada."""
    import ipaddress

    while True:
        ip_raw = input(f"  IP objetivo: ").strip()
        try:
            ip = str(ipaddress.ip_address(ip_raw))
            break
        except ValueError:
            error(f"'{ip_raw}' no es una IP válida.")

    while True:
        try:
            puerto = int(input(f"  Puerto [1-65535]: ").strip())
            if 1 <= puerto <= 65535:
                break
            error("El puerto debe estar entre 1 y 65535.")
        except ValueError:
            error("Ingresá un número entero.")

    ok(f"Escaneando {ip}:{puerto}... (simulado)")


def flujo_autenticacion():
    """Solicita usuario y contraseña, ocultando la contraseña con getpass."""
    usuario = input("  Usuario: ").strip()
    if not usuario:
        error("El usuario no puede estar vacío.")
        return

    clave = getpass.getpass("  Contraseña: ")

    # Simulación de verificación
    if usuario == "admin" and clave == "demo1234":
        ok(f"Acceso concedido para el usuario '{usuario}'")
    else:
        error("Credenciales incorrectas.")


mostrar_menu()
opcion = pedir_opcion()

if opcion == "1":
    flujo_escaneo()
elif opcion == "2":
    flujo_autenticacion()
else:
    info("Saliendo del framework...")

print(f"\n{MG}{'─' * ANCHO}{R}\n")