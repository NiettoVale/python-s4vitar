#!/usr/bin/env python3

import json
import ipaddress


# ---------------------------------------------------------------------------
# 1. try / except básico: lectura de un wordlist inexistente
# ---------------------------------------------------------------------------
print("== 1. try / except básico ==")

ruta_wordlist = "/usr/share/wordlists/no_existe.txt"

try:
    with open(ruta_wordlist, "r") as archivo:
        contenido = archivo.readlines()
        print(f"Wordlist cargado con {len(contenido)} líneas")
except FileNotFoundError:
    print(f"No se encontró el archivo de wordlist: {ruta_wordlist}")


# ---------------------------------------------------------------------------
# 2. Múltiples except: parsear una respuesta JSON de una API
# ---------------------------------------------------------------------------
print("\n== 2. Múltiples except ==")

def procesar_respuesta_api(texto_respuesta):
    try:
        datos = json.loads(texto_respuesta)
        cve_id = datos["cve_id"]
        severidad = datos["severidad"]
        print(f"CVE procesado: {cve_id} (severidad: {severidad})")
    except json.JSONDecodeError:
        print("La respuesta recibida no es un JSON válido")
    except KeyError as clave_faltante:
        print(f"La respuesta no contiene el campo esperado: {clave_faltante}")

# Caso 1: JSON malformado
procesar_respuesta_api('{"cve_id": "CVE-2024-1234", "severidad": ')

# Caso 2: JSON válido pero le falta un campo esperado
procesar_respuesta_api('{"cve_id": "CVE-2024-1234"}')

# Caso 3: respuesta correcta
procesar_respuesta_api('{"cve_id": "CVE-2024-1234", "severidad": "alta"}')


# ---------------------------------------------------------------------------
# 3. except Exception genérico: cálculo de estadísticas con datos vacíos
# ---------------------------------------------------------------------------
print("\n== 3. except Exception genérico ==")

def calcular_tiempo_promedio(tiempos_respuesta):
    try:
        promedio = sum(tiempos_respuesta) / len(tiempos_respuesta)
        print(f"Tiempo de respuesta promedio: {promedio:.3f} seg")
    except Exception as error:
        print(f"No se pudo calcular el promedio: {error}")

calcular_tiempo_promedio([0.12, 0.34, 0.21])
calcular_tiempo_promedio([])   # provoca ZeroDivisionError


# ---------------------------------------------------------------------------
# 4. else: validar el formato de una dirección IP
# ---------------------------------------------------------------------------
print("\n== 4. else en try/except ==")

def agregar_objetivo(direccion, lista_objetivos):
    try:
        ip_validada = ipaddress.ip_address(direccion)
    except ValueError:
        print(f"'{direccion}' no es una dirección IP válida, se descarta")
    else:
        # Solo se ejecuta si ip_address() no lanzó excepción
        lista_objetivos.append(str(ip_validada))
        print(f"'{direccion}' agregada como objetivo válido")

objetivos = []
agregar_objetivo("192.168.1.10", objetivos)
agregar_objetivo("999.999.999.999", objetivos)
agregar_objetivo("10.0.0.5", objetivos)

print(f"Objetivos finales: {objetivos}")


# ---------------------------------------------------------------------------
# 5. finally: garantizar el cierre de un archivo de reporte
# ---------------------------------------------------------------------------
print("\n== 5. finally ==")

def guardar_hallazgo(ruta_reporte, hallazgo):
    archivo = open(ruta_reporte, "a")
    try:
        if not isinstance(hallazgo, str):
            raise TypeError("El hallazgo debe ser una cadena de texto")
        archivo.write(hallazgo + "\n")
        print(f"Hallazgo guardado en {ruta_reporte}")
    except TypeError as error:
        print(f"No se pudo guardar el hallazgo: {error}")
    finally:
        archivo.close()
        print("Archivo de reporte cerrado correctamente")

guardar_hallazgo("/tmp/reporte_demo.txt", "Puerto 445 vulnerable a EternalBlue")
guardar_hallazgo("/tmp/reporte_demo.txt", 12345)   # tipo incorrecto, dispara el error


# ---------------------------------------------------------------------------
# 6. raise: validar un rango de red en notación CIDR
# ---------------------------------------------------------------------------
print("\n== 6. raise ==")

def validar_red(rango_cidr):
    """Valida que el rango de red tenga una notación CIDR correcta."""
    try:
        red = ipaddress.ip_network(rango_cidr, strict=False)
    except ValueError:
        raise ValueError(f"Rango de red inválido: '{rango_cidr}'")
    return red

try:
    red_valida = validar_red("192.168.1.0/24")
    print(f"Red válida para escaneo: {red_valida}")
except ValueError as error:
    print(f"Error: {error}")

try:
    validar_red("192.168.1.0/abc")
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------------------
# 7. Excepciones personalizadas: límite de intentos de autenticación
# ---------------------------------------------------------------------------
print("\n== 7. Excepciones personalizadas ==")

class LimiteIntentosExcedidoError(Exception):
    """Se levanta cuando se supera la cantidad máxima de intentos permitidos."""
    pass

def probar_credenciales(usuario, intentos_realizados, maximo_intentos=3):
    if intentos_realizados >= maximo_intentos:
        raise LimiteIntentosExcedidoError(
            f"Se alcanzó el máximo de {maximo_intentos} intentos para el usuario '{usuario}'"
        )
    print(f"Probando credencial #{intentos_realizados + 1} para '{usuario}'...")

intentos = 0
usuario_objetivo = "admin"

try:
    while True:
        probar_credenciales(usuario_objetivo, intentos)
        intentos += 1
except LimiteIntentosExcedidoError as error:
    print(f"Deteniendo ataque de fuerza bruta: {error}")
