#!/usr/bin/env python3
import re

WIDTH = 60

def section(title):
    print(f"\n{'═' * WIDTH}")
    print(f" {title}")
    print(f"{'═' * WIDTH}")

def sub(title):
    print(f"\n  ── {title}")


# ═════════════════════════════════════════════════════════════
# 1. FORMATEO DE CADENAS: %, format() y f-strings
# ═════════════════════════════════════════════════════════════
section("1. FORMATEO DE CADENAS")

# ── 1a. Operador % (estilo clásico, común en código heredado) ──
host     = "192.168.1.10"
port     = 8080
risk     = 9.5

sub("Operador % (estilo printf/C)")
print("  Host   : %s"   % host)
print("  Puerto : %d"   % port)
print("  Riesgo : %.1f" % risk)
print("  Resumen: [%s:%d] — Riesgo %.1f/10" % (host, port, risk))

# ── 1b. Método format() — útil para plantillas reutilizables ──
sub("Método format()")

# Plantilla reutilizable: se define una vez y se rellena con distintos datos
ALERT_TEMPLATE = "[{severity}] {cve} en {host}:{port} — CVSS: {cvss}"

alerts = [
    {"severity": "CRÍTICO", "cve": "CVE-2020-1472", "host": "192.168.1.10", "port": 445,  "cvss": 10.0},
    {"severity": "ALTO",    "cve": "CVE-2021-41773","host": "192.168.1.12", "port": 443,  "cvss": 9.8},
    {"severity": "MEDIO",   "cve": "CVE-2022-26134","host": "10.10.10.5",   "port": 8080, "cvss": 7.5},
]

for alert in alerts:
    print("  " + ALERT_TEMPLATE.format(**alert))

# Alineación de columnas con format()
sub("Alineación de columnas con format()")
print("  {:<18}{:<8}{:<12}{}".format("HOST", "PUERTO", "SERVICIO", "CVSS"))
print("  " + "─" * 44)
scan_rows = [
    ("192.168.1.10", 22,   "ssh",   6.5),
    ("192.168.1.10", 445,  "smb",  10.0),
    ("10.10.10.5",   8080, "http",  7.5),
]
for h, p, svc, cvss in scan_rows:
    print("  {:<18}{:<8}{:<12}{}".format(h, p, svc, cvss))

# ── 1c. F-strings — el estándar actual ──
sub("F-strings: interpolación directa de expresiones")

engagement = "Empresa S.A."
total_hosts = 24
active_hosts = 17
elapsed_seconds = 183.47

print(f"  Engagement    : {engagement}")
print(f"  Hosts totales : {total_hosts}")
print(f"  Hosts activos : {active_hosts} ({active_hosts/total_hosts*100:.1f}%)")
print(f"  Tiempo total  : {elapsed_seconds:.2f}s ({elapsed_seconds/60:.1f} min)")

# Relleno, alineación y bases numéricas en f-strings
byte_val = 255
print(f"\n  Byte 255 en distintas bases:")
print(f"    Decimal     : {byte_val:3d}")
print(f"    Hexadecimal : {byte_val:#04x}")
print(f"    Binario     : {byte_val:08b}")
print(f"    Octal       : {byte_val:#o}")

# Especificador = para depuración (Python 3.8+)
sub("Especificador = para depuración rápida")
target_ip   = "192.168.1.10"
open_ports  = [22, 80, 443]
print(f"  {target_ip=}")
print(f"  {open_ports=}")
print(f"  {len(open_ports)=}")


# ═════════════════════════════════════════════════════════════
# 2. strip / lstrip / rstrip
# ═════════════════════════════════════════════════════════════
section("2. strip / lstrip / rstrip")

# Limpieza de líneas crudas de un log simulado
raw_log_lines = [
    "   [2026-06-21] Acceso SSH desde 10.0.0.5   \n",
    "\t[2026-06-21] Intento fallido: root        \n",
    "   [2026-06-21] Puerto 3389 abierto          \n",
]

sub("Limpiar líneas de un log (strip)")
for line in raw_log_lines:
    clean = line.strip()
    print(f"  {clean}")

sub("strip() con caracteres específicos")
# Quitar guiones de un hash o identificador recibido de una API
raw_hash = "---d41d8cd98f00b204e9800998ecf8427e---"
print(f"  Hash limpio: {raw_hash.strip('-')}")

# Quitar comillas de un valor extraído de una respuesta JSON manual
raw_value = '"CVE-2023-23397"'
print(f"  CVE limpio: {raw_value.strip(chr(34))}")   # chr(34) = "


# ═════════════════════════════════════════════════════════════
# 3. upper / lower / capitalize / swapcase / title
# ═════════════════════════════════════════════════════════════
section("3. TRANSFORMACIONES DE CASO")

sub("Normalización para comparación de datos")
# Los nombres de usuario y servicios pueden venir en cualquier caso
raw_usernames = ["ADMIN", "Root", "service_BACKUP", "www-Data"]
normalized = [u.lower() for u in raw_usernames]
print(f"  Originales : {raw_usernames}")
print(f"  Normalizados: {normalized}")

sub("upper() para encabezados de tabla")
headers = ["host", "puerto", "protocolo", "estado"]
print("  " + " | ".join(h.upper() for h in headers))

sub("capitalize() y title() para nombres de vulnerabilidades")
vuln_names = ["sql injection", "path traversal", "xxe injection", "ssrf"]
for vuln in vuln_names:
    print(f"  {vuln:<20} → capitalize: {vuln.capitalize():<25} | title: {vuln.title()}")

sub("swapcase() para mutación de payloads")
# Técnica de evasión de filtros que comparan exactamente mayúsculas/minúsculas
payloads = ["<SCRIPT>alert(1)</SCRIPT>", "SELECT * FROM users", "cmd.exe /c whoami"]
for p in payloads:
    print(f"  {p:<35} → {p.swapcase()}")


# ═════════════════════════════════════════════════════════════
# 4. replace / split / join
# ═════════════════════════════════════════════════════════════
section("4. replace / split / join")

sub("replace(): redactar información sensible en un log")
audit_log = (
    "Usuario admin inició sesión desde 192.168.1.10 "
    "con token=eyJhbGciOiJIUzI1NiJ9.abc123"
)
# Redactar IP y token para exportar el log de forma segura
safe_log = audit_log.replace("192.168.1.10", "[IP_REDACTED]")
token_start = safe_log.find("token=")
if token_start != -1:
    safe_log = safe_log[:token_start] + "token=[TOKEN_REDACTED]"
print(f"  Log original : {audit_log}")
print(f"  Log redactado: {safe_log}")

sub("split(): parsear la salida de herramientas de red")
# Formato típico de una línea de nmap -oG (greppable output)
nmap_grepable = "Host: 192.168.1.10 (empresa.local)\tPorts: 22/open/tcp//ssh//OpenSSH 8.2/"

parts = nmap_grepable.split("\t")
host_part = parts[0].split()[1]   # "192.168.1.10"
ports_part = parts[1].replace("Ports: ", "").split("/")
port_number  = ports_part[0]
port_state   = ports_part[1]
port_service = ports_part[4]

print(f"  Host   : {host_part}")
print(f"  Puerto : {port_number} ({port_state}) — {port_service}")

sub("split() para parsear /etc/passwd")
passwd_entries = [
    "root:x:0:0:root:/root:/bin/bash",
    "www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin",
    "svc_backup:x:1001:1001::/home/svc_backup:/bin/sh",
]
print(f"  {'USUARIO':<15}{'UID':<6}{'SHELL'}")
print("  " + "─" * 35)
for entry in passwd_entries:
    fields = entry.split(":")
    print(f"  {fields[0]:<15}{fields[2]:<6}{fields[6]}")

sub("join(): construir comandos y payloads desde partes")
# Reconstruir una URL desde sus componentes
url_parts  = ["https", "empresa.com", "api", "v1", "users"]
url_built  = url_parts[0] + "://" + "/".join(url_parts[1:])
print(f"  URL construida: {url_built}")

# Construir una línea CSV desde campos individuales
csv_fields = ["192.168.1.10", "445", "smb", "CVE-2020-1472", "10.0"]
print(f"  CSV: {','.join(csv_fields)}")


# ═════════════════════════════════════════════════════════════
# 5. startswith / endswith / find / index / count
# ═════════════════════════════════════════════════════════════
section("5. startswith / endswith / find / index / count")

sub("startswith(): clasificar entradas por tipo")
mixed_entries = [
    "https://empresa.com",
    "http://old.empresa.com",
    "ftp://files.empresa.com",
    "# comentario ignorado",
    "192.168.1.10",
]
for entry in mixed_entries:
    if entry.startswith("#"):
        print(f"  [SKIP] {entry}")
    elif entry.startswith("https"):
        print(f"  [OK]   {entry}")
    elif entry.startswith(("http://", "ftp://")):
        print(f"  [WARN] Protocolo inseguro: {entry}")
    else:
        print(f"  [IP]   {entry}")

sub("endswith(): filtrar archivos por extensión")
file_list = [
    "payload.exe", "readme.md", "shell.php",
    "config.bak", "index.html", "exploit.py",
]
dangerous_ext = (".exe", ".php", ".py", ".sh", ".bat")
for fname in file_list:
    tag = "[!] SOSPECHOSO" if fname.endswith(dangerous_ext) else "[+] OK"
    print(f"  {tag:<18} {fname}")

sub("find() para extraer valores de cabeceras HTTP")
http_response = (
    "HTTP/1.1 200 OK\r\n"
    "Server: Apache/2.4.51 (Unix) OpenSSL/1.1.1\r\n"
    "X-Powered-By: PHP/7.4.3\r\n"
    "Content-Type: text/html\r\n"
)

for header_name in ["Server", "X-Powered-By", "X-Frame-Options"]:
    pos = http_response.find(header_name + ":")
    if pos != -1:
        # Extraer el valor hasta el fin de esa línea
        end_pos = http_response.find("\r\n", pos)
        value   = http_response[pos + len(header_name) + 2:end_pos]
        print(f"  {header_name:<20}: {value}")
    else:
        print(f"  {header_name:<20}: [no presente — puede ser una buena práctica]")

sub("count(): análisis de frecuencia en logs")
auth_log = (
    "Jun 21 FAILED root 203.0.113.5 | "
    "Jun 21 FAILED admin 203.0.113.5 | "
    "Jun 21 FAILED root 203.0.113.5 | "
    "Jun 21 SUCCESS root 10.0.0.1 | "
    "Jun 21 FAILED root 203.0.113.5"
)
failed  = auth_log.count("FAILED")
success = auth_log.count("SUCCESS")
ip_hits = auth_log.count("203.0.113.5")
print(f"  Intentos fallidos: {failed}")
print(f"  Accesos exitosos : {success}")
print(f"  Hits de 203.0.113.5: {ip_hits} → {'posible brute-force' if ip_hits > 2 else 'normal'}")


# ═════════════════════════════════════════════════════════════
# 6. MÉTODOS is* / in / not in
# ═════════════════════════════════════════════════════════════
section("6. MÉTODOS is* / in / not in")

sub("isdigit() para validar entradas numéricas")
user_inputs = ["443", "8080", "abc", "", "65536", "22"]
for value in user_inputs:
    if not value.isdigit():
        print(f"  [ERROR] '{value}' no es un número")
    elif not (1 <= int(value) <= 65535):
        print(f"  [ERROR] '{value}' fuera del rango válido [1-65535]")
    else:
        print(f"  [OK]    Puerto válido: {value}")

sub("isalnum() para validar nombres de usuario")
usernames = ["admin", "user_123", "hacker!", "root", "sys-admin"]
for u in usernames:
    # Los nombres de usuario solo deberían contener alfanuméricos (para esta validación simple)
    if u.replace("_", "").replace("-", "").isalnum():
        print(f"  [OK]    '{u}'")
    else:
        print(f"  [WARN]  '{u}' contiene caracteres especiales")

sub("in / not in para detección de keywords en payloads")
payloads_to_analyze = [
    "GET /index.php?id=1 HTTP/1.1",
    "GET /search?q=<script>alert(1)</script> HTTP/1.1",
    "GET /api/v1/users?filter=1 OR 1=1-- HTTP/1.1",
    "GET /home HTTP/1.1",
]
sqli_patterns = ["OR 1=1", "UNION SELECT", "DROP TABLE", "--", "/*"]
xss_patterns  = ["<script", "alert(", "onerror=", "javascript:"]

for req in payloads_to_analyze:
    sqli = [p for p in sqli_patterns if p.lower() in req.lower()]
    xss  = [p for p in xss_patterns  if p.lower() in req.lower()]
    if sqli:
        print(f"  [SQLi]  {req[:55]} → {sqli}")
    elif xss:
        print(f"  [XSS]   {req[:55]} → {xss}")
    else:
        print(f"  [OK]    {req[:55]}")


# ═════════════════════════════════════════════════════════════
# 7. maketrans / translate
# ═════════════════════════════════════════════════════════════
section("7. maketrans / translate")

sub("Cifrado de sustitución simple (Caesar cipher)")
# Desplazamiento de 3 posiciones (ROT3)
alphabet = "abcdefghijklmnopqrstuvwxyz"
shifted  = "defghijklmnopqrstuvwxyzabc"
caesar_table = str.maketrans(
    alphabet + alphabet.upper(),
    shifted  + shifted.upper()
)

plaintext  = "AttackAtDawn"
ciphertext = plaintext.translate(caesar_table)
print(f"  Texto plano : {plaintext}")
print(f"  Cifrado     : {ciphertext}")

sub("Eliminar caracteres no deseados de un payload")
# Sanitizar una cadena eliminando caracteres que no deberían aparecer en un input
raw_input = "  <admin>; DROP TABLE users; --  "
# Eliminar espacios, puntuación peligrosa y etiquetas HTML en una sola pasada
remove_chars = str.maketrans("", "", " <>;-\"'")
sanitized = raw_input.translate(remove_chars)
print(f"  Input original  : {raw_input!r}")
print(f"  Input saneado   : {sanitized!r}")

sub("Normalización de caracteres confundibles (homoglyph attack)")
# En ataques de homoglyph, se usan caracteres Unicode que parecen iguales
# a letras latinas para engañar comparaciones de nombres de dominio o usuario
homoglyph_table = str.maketrans("0O1lI", "oolis")   # cero→o, O→o, 1→o, l→i, I→i
suspicious_domains = ["аmazon.com", "g00gle.com", "paypаl.com"]
for domain in suspicious_domains:
    normalized = domain.translate(homoglyph_table)
    flag = "[WARN] Posible homoglyph" if normalized != domain else "[OK]"
    print(f"  {flag}: '{domain}' → '{normalized}'")


# ═════════════════════════════════════════════════════════════
# 8. EXPRESIONES REGULARES con re
# ═════════════════════════════════════════════════════════════
section("8. EXPRESIONES REGULARES (módulo re)")

sub("Extraer IPs y puertos de la salida de un escáner")
scanner_output = """
Nmap scan report for 192.168.1.10
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https

Nmap scan report for 10.0.0.5
3389/tcp open  ms-wbt-server
8080/tcp open  http-proxy
"""

# Extraer IPs
ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", scanner_output)
print(f"  IPs detectadas: {list(dict.fromkeys(ips))}")   # deduplicadas con dict

# Extraer pares puerto/servicio con grupos de captura
port_pattern = re.compile(r"(\d+)/tcp\s+open\s+(\S+)")
print(f"  {'PUERTO':<10}{'SERVICIO'}")
print("  " + "─" * 24)
for match in port_pattern.finditer(scanner_output):
    port, service = match.groups()
    print(f"  {port:<10}{service}")

sub("Extraer emails de un dump de texto")
email_dump = """
Contactos encontrados en el sitio:
  info@empresa.com, admin@empresa.com
  soporte.tecnico@empresa.com
  noreply@no-responder.org
"""
emails = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", email_dump)
print(f"  Emails extraídos: {emails}")

sub("Redactar IPs en un reporte antes de compartirlo")
report_with_ips = (
    "El host 192.168.1.10 expone SMB. "
    "Desde 10.0.0.5 se detectó un escaneo. "
    "El gateway 192.168.1.1 no responde."
)
ip_pattern  = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
redacted    = re.sub(ip_pattern, "[IP_REDACTADA]", report_with_ips)
print(f"  Original : {report_with_ips}")
print(f"  Redactado: {redacted}")

sub("Validar formatos con re.match")
patterns = {
    "IPv4"  : r"^\d{1,3}(\.\d{1,3}){3}$",
    "CVE"   : r"^CVE-\d{4}-\d{4,7}$",
    "SHA256": r"^[a-fA-F0-9]{64}$",
    "Puerto": r"^([1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$",
}
test_values = [
    ("192.168.1.10",                                               "IPv4"),
    ("CVE-2020-1472",                                              "CVE"),
    ("d41d8cd98f00b204e9800998ecf8427e9800998ecf8427eaabbccdd1122", "SHA256"),
    ("443",                                                        "Puerto"),
    ("99999",                                                      "Puerto"),
]
for value, expected_type in test_values:
    pattern = patterns.get(expected_type, "")
    valid   = bool(re.match(pattern, value))
    status  = "[OK]" if valid else "[INVÁLIDO]"
    print(f"  {status:<12} {expected_type:<8}: '{value}'")
