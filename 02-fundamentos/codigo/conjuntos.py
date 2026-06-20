#!/usr/bin/env python3
import time

ANCHO = 70


def titulo(texto):
    print("\n" + "═" * ANCHO)
    print(f" {texto}")
    print("═" * ANCHO)


def subtitulo(texto):
    print(f"\n── {texto} {'─' * (ANCHO - len(texto) - 4)}")


# ---------------------------------------------------------------------------
# 1. Unicidad: deduplicar hashes de archivos analizados
# ---------------------------------------------------------------------------
titulo("1. Unicidad automática")

hashes_md5_analizados = {
    "5d41402abc4b2a76b9719d911017c592",
    "7d793037a0760186574b0282f2f435e7",
    "5d41402abc4b2a76b9719d911017c592",   # duplicado, será descartado solo
}

subtitulo("Resultado")
print(f"  Cantidad de hashes únicos: {len(hashes_md5_analizados)}")
for h in hashes_md5_analizados:
    print(f"    {h}")


# ---------------------------------------------------------------------------
# 2. Restricción de hashabilidad: qué SÍ y qué NO puede ir en un set
# ---------------------------------------------------------------------------
titulo("2. Restricción de hashabilidad")

subtitulo("Válido: cadenas y tuplas (inmutables)")
permisos_validos = {"read", ("write", "admin")}
print(f"  {permisos_validos}")

subtitulo("Inválido: una lista dentro de un set (capturado)")
try:
    conjunto_invalido = {[22, 80, 443]}
except TypeError as error:
    print(f"  Error capturado: {error}")


# ---------------------------------------------------------------------------
# 3. add() / discard() / remove(): gestión de una blacklist de IPs
# ---------------------------------------------------------------------------
titulo("3. Gestión de una blacklist de IPs")

blacklist = {"185.220.101.5", "194.165.16.3"}

blacklist.add("91.243.85.17")
subtitulo("Tras agregar una IP nueva")
print(f"  {blacklist}")

blacklist.discard("10.0.0.1")   # no existe, pero no rompe nada
subtitulo("Tras discard() de una IP inexistente (sin error)")
print(f"  {blacklist}")

try:
    blacklist.remove("10.0.0.1")   # esta sí rompe, porque no existe
except KeyError as error:
    subtitulo("Tras remove() de una IP inexistente (capturado)")
    print(f"  Error capturado: {error}")


# ---------------------------------------------------------------------------
# 4. Unión: consolidar IOCs de dos feeds de threat intelligence
# ---------------------------------------------------------------------------
titulo("4. Unión de conjuntos")

feed_alfa = {"45.137.21.9", "185.220.101.5", "91.243.85.17"}
feed_beta = {"185.220.101.5", "194.165.16.3", "23.129.64.131"}

consolidado = feed_alfa | feed_beta

subtitulo("IOCs consolidados (sin duplicados)")
for ip in sorted(consolidado):
    print(f"  {ip}")
print(f"\n  Total: {len(consolidado)} IPs únicas")


# ---------------------------------------------------------------------------
# 5. Intersección: IOCs confirmados por ambos feeds
# ---------------------------------------------------------------------------
titulo("5. Intersección de conjuntos")

confirmados_por_ambos = feed_alfa & feed_beta

subtitulo("IPs reportadas por AMBOS feeds (mayor confianza)")
for ip in confirmados_por_ambos:
    print(f"  [!!] {ip}")


# ---------------------------------------------------------------------------
# 6. Diferencia: IOCs exclusivos de un solo feed
# ---------------------------------------------------------------------------
titulo("6. Diferencia de conjuntos")

solo_alfa = feed_alfa - feed_beta
solo_beta = feed_beta - feed_alfa

subtitulo("Exclusivos de cada feed")
print(f"  Solo en feed_alfa: {solo_alfa}")
print(f"  Solo en feed_beta: {solo_beta}")


# ---------------------------------------------------------------------------
# 7. Diferencia simétrica: discrepancias totales entre dos escaneos
# ---------------------------------------------------------------------------
titulo("7. Diferencia simétrica")

hosts_escaneo_lunes = {"192.168.1.10", "192.168.1.11", "192.168.1.12"}
hosts_escaneo_viernes = {"192.168.1.11", "192.168.1.12", "192.168.1.13"}

discrepancias = hosts_escaneo_lunes ^ hosts_escaneo_viernes

subtitulo("Hosts que cambiaron de estado entre escaneos")
for host in sorted(discrepancias):
    if host in hosts_escaneo_lunes:
        print(f"  {host}: desapareció (estaba el lunes, no el viernes)")
    else:
        print(f"  {host}: apareció (no estaba el lunes, sí el viernes)")


# ---------------------------------------------------------------------------
# 8. Subconjuntos: validar cobertura de hardening
# ---------------------------------------------------------------------------
titulo("8. Subconjuntos: validar checklist de hardening")

controles_requeridos = {"firewall_activo", "logs_centralizados", "mfa_habilitado"}
controles_implementados = {"firewall_activo", "logs_centralizados", "mfa_habilitado", "backup_diario"}

subtitulo("¿Se cumplen todos los controles requeridos?")
cumple = controles_requeridos.issubset(controles_implementados)
print(f"  Cumple checklist mínimo: {cumple}")

faltantes = controles_requeridos - controles_implementados
print(f"  Controles faltantes: {faltantes if faltantes else 'ninguno'}")


# ---------------------------------------------------------------------------
# 9. Rendimiento: pertenencia en set vs. lista
# ---------------------------------------------------------------------------
titulo("9. Rendimiento: verificación de pertenencia")

ips_maliciosas_lista = [f"203.0.{i}.{j}" for i in range(0, 100) for j in range(0, 100)]
ips_maliciosas_set = set(ips_maliciosas_lista)
ip_objetivo = "203.0.99.99"   # peor caso: al final de la lista

inicio = time.perf_counter()
ip_objetivo in ips_maliciosas_lista
tiempo_lista = time.perf_counter() - inicio

inicio = time.perf_counter()
ip_objetivo in ips_maliciosas_set
tiempo_set = time.perf_counter() - inicio

subtitulo(f"Buscando 1 IP entre {len(ips_maliciosas_lista):,} registros")
print(f"  Tiempo con lista (O(n)): {tiempo_lista:.8f} seg")
print(f"  Tiempo con set   (O(1)): {tiempo_set:.8f} seg")
print(f"  El set fue ~{tiempo_lista / tiempo_set:.0f}x más rápido en esta prueba")


# ---------------------------------------------------------------------------
# 10. frozenset: perfiles de permisos como elementos de otro conjunto
# ---------------------------------------------------------------------------
titulo("10. frozenset: perfiles de permisos inmutables")

perfil_lectura = frozenset({"read"})
perfil_operador = frozenset({"read", "write"})
perfil_admin = frozenset({"read", "write", "delete", "manage_users"})

perfiles_detectados_en_sistema = {perfil_lectura, perfil_admin}

subtitulo("Perfiles únicos detectados (un frozenset puede vivir dentro de un set)")
for perfil in perfiles_detectados_en_sistema:
    print(f"  {set(perfil)}")

print(f"\n  ¿El perfil 'operador' ya fue visto? {perfil_operador in perfiles_detectados_en_sistema}")


# ---------------------------------------------------------------------------
# 11. Comprensión de conjuntos: extraer dominios únicos de una lista
# ---------------------------------------------------------------------------
titulo("11. Comprensión de conjuntos")

urls_visitadas = [
    "http://login.empresa.com/portal",
    "http://login.empresa.com/api",
    "http://intranet.empresa.com",
    "http://LOGIN.empresa.com/portal",
]

dominios_unicos = {url.split("//")[1].split("/")[0].lower() for url in urls_visitadas}

subtitulo("Dominios únicos extraídos de las URLs visitadas")
for dominio in dominios_unicos:
    print(f"  {dominio}")