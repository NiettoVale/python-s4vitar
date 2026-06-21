#!/usr/bin/env python3


# ---------------------------------------------------------------------------
# 1. Ámbito local: variables que solo existen dentro de la función
# ---------------------------------------------------------------------------
print("== 1. Ámbito local ==")

def analizar_host(host):
    estado = "activo"   # variable local, solo existe dentro de esta función
    print(f"{host}: {estado}")

analizar_host("192.168.1.10")
analizar_host("192.168.1.11")

# Intentar acceder a 'estado' aquí afuera produciría un error,
# ya que esa variable no existe en este ámbito:
# print(estado)  # NameError: name 'estado' is not defined
print("La variable 'estado' no existe fuera de analizar_host()")


# ---------------------------------------------------------------------------
# 2. Ámbito global: variables accesibles (en lectura) desde cualquier función
# ---------------------------------------------------------------------------
print("\n== 2. Ámbito global (lectura) ==")

red_objetivo = "192.168.1.0/24"   # variable global

def mostrar_objetivo():
    # Se puede LEER una variable global sin declararla explícitamente
    print(f"Red objetivo del escaneo: {red_objetivo}")

mostrar_objetivo()


# ---------------------------------------------------------------------------
# 3. El error común: intentar modificar una global sin declararla
# ---------------------------------------------------------------------------
print("\n== 3. Error al modificar una variable global sin 'global' ==")

contador_hosts_activos = 0   # variable global

def registrar_host_activo_con_error():
    try:
        # Esto NO modifica la variable global; Python intenta crear
        # una variable local con el mismo nombre, lo que produce un error
        # porque se usa antes de haber sido asignada en este ámbito
        contador_hosts_activos = contador_hosts_activos + 1
    except UnboundLocalError as error:
        print(f"Error capturado: {error}")

registrar_host_activo_con_error()
print(f"Valor de la variable global, sin modificar: {contador_hosts_activos}")


# ---------------------------------------------------------------------------
# 4. Uso correcto de 'global' para modificar una variable global
# ---------------------------------------------------------------------------
print("\n== 4. Uso correcto de 'global' ==")

contador_hosts_activos = 0   # reiniciamos la variable global

def registrar_host_activo():
    global contador_hosts_activos
    contador_hosts_activos += 1   # ahora sí modifica la variable global

registrar_host_activo()
registrar_host_activo()
registrar_host_activo()

print(f"Hosts activos registrados: {contador_hosts_activos}")   # 3


# ---------------------------------------------------------------------------
# 5. Alternativa recomendada: usar return en lugar de 'global'
# ---------------------------------------------------------------------------
print("\n== 5. Alternativa recomendada: return en vez de global ==")

def incrementar_contador(valor_actual):
    """En lugar de depender de 'global', recibe el valor y devuelve el nuevo."""
    return valor_actual + 1

contador_hosts_activos = 0
contador_hosts_activos = incrementar_contador(contador_hosts_activos)
contador_hosts_activos = incrementar_contador(contador_hosts_activos)
contador_hosts_activos = incrementar_contador(contador_hosts_activos)

print(f"Hosts activos registrados (con return): {contador_hosts_activos}")   # 3