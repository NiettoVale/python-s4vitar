#!/usr/bin/env python3

# ---------------------------------------------------------------------------
# 1. Función básica con return
# ---------------------------------------------------------------------------
print("== 1. Función básica con return ==")

def es_puerto_critico(puerto):
    """Devuelve True si el puerto pertenece a la lista de puertos críticos conocidos."""
    puertos_criticos = [21, 23, 445, 3389]
    return puerto in puertos_criticos

print(f"¿Puerto 445 es crítico? {es_puerto_critico(445)}")
print(f"¿Puerto 80 es crítico?  {es_puerto_critico(80)}")


# ---------------------------------------------------------------------------
# 2. Parámetros posicionales
# ---------------------------------------------------------------------------
print("\n== 2. Parámetros posicionales ==")

def conectar(host, puerto, protocolo):
    print(f"Conectando a {host} en el puerto {puerto} usando {protocolo}")

# Los argumentos se asignan en el mismo orden en que fueron definidos
conectar("192.168.1.10", 443, "https")


# ---------------------------------------------------------------------------
# 3. Parámetros por clave (keyword arguments)
# ---------------------------------------------------------------------------
print("\n== 3. Parámetros por clave ==")

# El orden ya no importa: se especifican por nombre
conectar(protocolo="https", host="192.168.1.10", puerto=443)

# Combinación de posicional + por clave (el posicional siempre va primero)
conectar("192.168.1.10", puerto=22, protocolo="ssh")


# ---------------------------------------------------------------------------
# 4. Valores por defecto
# ---------------------------------------------------------------------------
print("\n== 4. Valores por defecto ==")

def conectar_con_defaults(host, puerto=443, protocolo="https"):
    print(f"Conectando a {host} en el puerto {puerto} usando {protocolo}")

conectar_con_defaults("192.168.1.10")                          # usa los valores por defecto
conectar_con_defaults("192.168.1.10", puerto=22, protocolo="ssh")  # los sobrescribe


# ---------------------------------------------------------------------------
# 5. *args: cantidad variable de argumentos posicionales
# ---------------------------------------------------------------------------
print("\n== 5. *args ==")

def escanear_puertos(host, *args):
    """Permite pasar una cantidad arbitraria de puertos a escanear."""
    print(f"Escaneando host {host} en los siguientes puertos:")
    for puerto in args:
        print(f"  -> Puerto {puerto}")

escanear_puertos("192.168.1.10", 22, 80)
escanear_puertos("192.168.1.10", 21, 22, 80, 443, 3389)


# ---------------------------------------------------------------------------
# 6. **kwargs: cantidad variable de argumentos por clave
# ---------------------------------------------------------------------------
print("\n== 6. **kwargs ==")

def registrar_hallazgo(host, **kwargs):
    """Permite registrar un hallazgo con una cantidad variable de atributos adicionales."""
    print(f"Hallazgo registrado en {host}:")
    for clave, valor in kwargs.items():
        print(f"  -> {clave}: {valor}")

registrar_hallazgo(
    "192.168.1.10",
    puerto=22,
    servicio="ssh",
    version="OpenSSH 7.2",
    severidad="alta",
)


# ---------------------------------------------------------------------------
# 7. Combinación de *args y **kwargs
# ---------------------------------------------------------------------------
print("\n== 7. *args + **kwargs combinados ==")

def ejecutar_modulo(nombre_modulo, *args, **kwargs):
    print(f"Ejecutando módulo: {nombre_modulo}")
    print(f"Argumentos posicionales: {args}")
    print(f"Argumentos por clave: {kwargs}")

ejecutar_modulo("port_scanner", "192.168.1.10", 22, 80, timeout=5, verbose=True)