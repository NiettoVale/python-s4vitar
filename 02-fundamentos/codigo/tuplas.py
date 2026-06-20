#!/usr/bin/env python3
from collections import namedtuple


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
# 1. Inmutabilidad: protegiendo la configuración de un escaneo
# ---------------------------------------------------------------------------
titulo("1. Inmutabilidad de las tuplas")

configuracion_base = ("192.168.1.0/24", 443, "https")

subtitulo("Intento de modificación (capturado)")
try:
    configuracion_base[1] = 8443
except TypeError as error:
    print(f"  Error capturado: {error}")
    print("  -> La configuración base del escaneo permanece intacta.")


# ---------------------------------------------------------------------------
# 2. Inmutabilidad superficial: una lista mutable dentro de una tupla
# ---------------------------------------------------------------------------
titulo("2. Inmutabilidad superficial")

registro_host = ("192.168.1.10", [22, 80])

subtitulo("Antes de modificar la lista interna")
print(f"  {registro_host}")

registro_host[1].append(443)   # válido: se modifica la lista, no la tupla

subtitulo("Después (la lista interna SÍ cambió)")
print(f"  {registro_host}")
print("  -> La tupla en sí no cambió de tamaño ni de referencias, pero su contenido mutable sí.")


# ---------------------------------------------------------------------------
# 3. Indexación y slicing: desglosar una tupla de configuración de red
# ---------------------------------------------------------------------------
titulo("3. Indexación y slicing")

interfaz_red = ("eth0", "192.168.1.50", "255.255.255.0", "192.168.1.1", "8.8.8.8")

subtitulo("Acceso individual")
print(f"  Interfaz:     {interfaz_red[0]}")
print(f"  Gateway:      {interfaz_red[-2]}")
print(f"  DNS:          {interfaz_red[-1]}")

subtitulo("Slicing (subsecuencia de red)")
datos_red = interfaz_red[1:4]
print(f"  IP/Máscara/Gateway: {datos_red}")


# ---------------------------------------------------------------------------
# 4. Tuplas como clave de diccionario: inventario de servicios
# ---------------------------------------------------------------------------
titulo("4. Tuplas como clave de diccionario")

inventario = {
    ("192.168.1.10", 22): "OpenSSH 8.2",
    ("192.168.1.10", 443): "nginx 1.18",
    ("192.168.1.11", 445): "Samba 4.6",
}

subtitulo("Consulta directa por (host, puerto)")
clave = ("192.168.1.10", 443)
print(f"  Servicio en {clave}: {inventario.get(clave, 'no registrado')}")

clave_inexistente = ("192.168.1.99", 21)
print(f"  Servicio en {clave_inexistente}: {inventario.get(clave_inexistente, 'no registrado')}")


# ---------------------------------------------------------------------------
# 5. Empaquetado y desempaquetado básico
# ---------------------------------------------------------------------------
titulo("5. Empaquetado y desempaquetado")

credencial = "admin", "S3cr3t!", "ssh"   # empaquetado sin paréntesis explícitos

usuario, contrasena, servicio = credencial   # desempaquetado

subtitulo("Resultado del desempaquetado")
print(f"  Usuario: {usuario}  |  Servicio: {servicio}  |  Contraseña: {'*' * len(contrasena)}")


# ---------------------------------------------------------------------------
# 6. Desempaquetado extendido con *
# ---------------------------------------------------------------------------
titulo("6. Desempaquetado extendido")

fila_escaneo = ("192.168.1.10", 21, 22, 80, 443, 445, 3389)

host, *puertos_abiertos = fila_escaneo

subtitulo("Separar el host del resto de los puertos")
print(f"  Host:    {host}")
print(f"  Puertos: {puertos_abiertos}")

primero, *intermedios, ultimo = fila_escaneo
subtitulo("Capturar primero, intermedios y último")
print(f"  Primer puerto: {primero}  |  Intermedios: {intermedios}  |  Último: {ultimo}")


# ---------------------------------------------------------------------------
# 7. Concatenación y repetición
# ---------------------------------------------------------------------------
titulo("7. Concatenación y repetición")

protocolos_capa_transporte = ("tcp", "udp")
protocolos_capa_red = ("icmp",)

todos_los_protocolos = protocolos_capa_transporte + protocolos_capa_red
print(f"  Concatenación: {todos_los_protocolos}")

separador = ("=",) * 20
print(f"  Repetición:    {''.join(separador)}")


# ---------------------------------------------------------------------------
# 8. index() y count()
# ---------------------------------------------------------------------------
titulo("8. index() y count()")

codigos_http_observados = (200, 404, 404, 301, 200, 200, 500)

subtitulo("Búsqueda en la tupla de códigos HTTP")
print(f"  Posición del primer 404: {codigos_http_observados.index(404)}")
print(f"  Cantidad de respuestas 200: {codigos_http_observados.count(200)}")


# ---------------------------------------------------------------------------
# 9. Función que devuelve múltiples valores como tupla
# ---------------------------------------------------------------------------
titulo("9. Función con retorno múltiple")

def analizar_certificado_tls(host):
    """Simula el análisis de un certificado TLS, devolviendo varios datos a la vez."""
    valido = True
    dias_para_expirar = 45
    emisor = "Let's Encrypt"
    return valido, dias_para_expirar, emisor

es_valido, dias_restantes, emisor_cert = analizar_certificado_tls("192.168.1.10")

subtitulo("Resultado del análisis")
print(f"  Válido: {es_valido}  |  Expira en: {dias_restantes} días  |  Emisor: {emisor_cert}")


# ---------------------------------------------------------------------------
# 10. Estructuras fijas: constantes de configuración de la herramienta
# ---------------------------------------------------------------------------
titulo("10. Estructuras fijas (constantes)")

PUERTOS_ESCANEO_RAPIDO = (21, 22, 23, 80, 443, 445, 3389)
CODIGOS_HTTP_RELEVANTES = (200, 301, 302, 401, 403, 500)

subtitulo("Constantes definidas para el módulo de escaneo")
print(f"  PUERTOS_ESCANEO_RAPIDO  = {PUERTOS_ESCANEO_RAPIDO}")
print(f"  CODIGOS_HTTP_RELEVANTES = {CODIGOS_HTTP_RELEVANTES}")


# ---------------------------------------------------------------------------
# 11. namedtuple: hallazgos con campos accesibles por nombre
# ---------------------------------------------------------------------------
titulo("11. namedtuple: hallazgos legibles por nombre de campo")

Hallazgo = namedtuple("Hallazgo", ["host", "puerto", "servicio", "cvss"])

hallazgos = [
    Hallazgo("192.168.1.10", 445, "smb", 10.0),
    Hallazgo("192.168.1.11", 22, "ssh", 6.5),
    Hallazgo("192.168.1.12", 443, "https", 4.2),
]

subtitulo("Listado de hallazgos (acceso por atributo, no por índice)")
for h in hallazgos:
    print(f"  {h.host:<16}{h.puerto:<8}{h.servicio:<8}CVSS {h.cvss:>4.1f}")

subtitulo("Filtrar usando los nombres de campo (más legible que índices numéricos)")
criticos = [h for h in hallazgos if h.cvss >= 9.0]
for h in criticos:
    print(f"  [!] {h.host}:{h.puerto} ({h.servicio}) - CVSS {h.cvss}")