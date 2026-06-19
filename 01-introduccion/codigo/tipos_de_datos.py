#!/usr/bin/env python3

# ---------------------------------------------------------------------------
# Strings: representación de datos textuales (host objetivo)
# ---------------------------------------------------------------------------
host_objetivo = "192.168.1.10"
print(host_objetivo)
print(type(host_objetivo))

# ---------------------------------------------------------------------------
# Integers y Floats: valores numéricos (costo de licencia y puerto principal)
# ---------------------------------------------------------------------------
costo_licencia = 34.55   # float: costo de una licencia de herramienta de pentesting
puerto_principal = 80    # int: puerto web detectado en el host objetivo

print(f'\n{costo_licencia}\n{puerto_principal}')

# ---------------------------------------------------------------------------
# Booleanos: estado de comprobaciones sobre el host
# ---------------------------------------------------------------------------
host_comprometido = False   # aún no se logró acceso al sistema
puerto_ssh_abierto = True   # el puerto 22 respondió como abierto

print(f'\n{host_comprometido}\n{puerto_ssh_abierto}')

# ---------------------------------------------------------------------------
# Listas: puertos abiertos detectados durante el escaneo
# ---------------------------------------------------------------------------
puertos_abiertos = []
puertos_abiertos.append(22)
puertos_abiertos.append(80)
puertos_abiertos.append(443)

print(puertos_abiertos)
print(f'Primer puerto detectado: {puertos_abiertos[0]}')

print("\nRecorrido de puertos abiertos en el host objetivo")
for puerto in puertos_abiertos:
    print(f'Puerto [{puerto}] abierto en {host_objetivo}')