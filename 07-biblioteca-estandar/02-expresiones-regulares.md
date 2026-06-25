# Expresiones Regulares en Python: el Módulo `re`

## Introducción

Las expresiones regulares (_regular expressions_, o _regex_) son patrones de búsqueda formales que permiten describir, de forma concisa y precisa, la estructura que debe tener una cadena de texto para ser considerada una coincidencia. El módulo `re` de la biblioteca estándar de Python implementa un motor de expresiones regulares completo, compatible con la sintaxis POSIX extendida y con extensiones adicionales propias de Perl.

En el ámbito de la ciberseguridad, las expresiones regulares aparecen en prácticamente todas las tareas de procesamiento de texto: extraer direcciones IP de la salida de un escáner, parsear líneas de `/var/log/auth.log` para detectar intentos de fuerza bruta, validar el formato de un CVE, redactar información sensible antes de exportar un log, identificar patrones de SQLi o XSS en tráfico HTTP, o extraer hashes, dominios y emails de un dump de texto. Dominar las expresiones regulares multiplica sustancialmente la capacidad de automatización de cualquier herramienta de análisis.

## Sintaxis de Expresiones Regulares

Antes de abordar las funciones del módulo `re`, es fundamental entender los bloques de construcción de los propios patrones. Una expresión regular es una cadena compuesta por caracteres literales y **metacaracteres**, que son símbolos con significados especiales dentro del patrón.

### Caracteres y Clases de Caracteres

```
.          Cualquier carácter excepto el salto de línea (\n)
\d         Cualquier dígito: equivalente a [0-9]
\D         Cualquier carácter que NO sea dígito: equivalente a [^0-9]
\w         Cualquier carácter de "palabra": letras, dígitos y guion bajo [a-zA-Z0-9_]
\W         Cualquier carácter que NO sea de "palabra"
\s         Cualquier espacio en blanco: espacio, tabulación, salto de línea
\S         Cualquier carácter que NO sea espacio en blanco
[abc]      Cualquiera de los caracteres entre corchetes (a, b o c)
[^abc]     Cualquier carácter que NO sea a, b ni c
[a-z]      Cualquier letra minúscula (rango)
[a-zA-Z]   Cualquier letra (mayúscula o minúscula)
[0-9]      Cualquier dígito (equivalente a \d)
```

### Cuantificadores

Los cuantificadores definen cuántas veces debe repetirse el elemento que preceden.

```
*          0 o más repeticiones (codicioso)
+          1 o más repeticiones (codicioso)
?          0 o 1 repetición (hace al elemento opcional)
{n}        Exactamente n repeticiones
{n,}       Al menos n repeticiones
{n,m}      Entre n y m repeticiones (inclusive)
*?         0 o más repeticiones (perezoso / no codicioso)
+?         1 o más repeticiones (perezoso / no codicioso)
```

La distinción entre **codicioso** (_greedy_) y **perezoso** (_lazy_) es importante: por defecto, los cuantificadores son codiciosos, es decir, intentan capturar la mayor cantidad de texto posible que siga cumpliendo el patrón. Al añadir `?` al cuantificador se lo convierte en perezoso, capturando la menor cantidad posible.

```python
import re

html = "<b>negrita</b> y <i>cursiva</i>"

# Cuantificador codicioso: captura desde el primer < hasta el último >
print(re.findall(r"<.+>", html))    # ['<b>negrita</b> y <i>cursiva</i>']

# Cuantificador perezoso: captura la etiqueta más corta posible
print(re.findall(r"<.+?>", html))   # ['<b>', '</b>', '<i>', '</i>']
```

### Anclas y Aserciones

Las anclas no consumen caracteres: verifican una condición de posición en la cadena.

```
^          Inicio de la cadena (o inicio de línea en modo multilínea)
$          Fin de la cadena (o fin de línea en modo multilínea)
\b         Frontera de palabra (entre \w y \W, o al inicio/fin de la cadena)
\B         No-frontera de palabra
(?=...)    Lookahead positivo: lo que sigue debe coincidir con ... (sin consumirlo)
(?!...)    Lookahead negativo: lo que sigue NO debe coincidir con ...
(?<=...)   Lookbehind positivo: lo que precede debe coincidir con ...
(?<!...)   Lookbehind negativo: lo que precede NO debe coincidir con ...
```

```python
import re

texto = "La IP 192.168.1.10 y la IP 10.0.0.5 están activas"

# \b garantiza que "10" no coincida dentro de "192.168.1.10" como número suelto
print(re.findall(r"\b10\.\d+\.\d+\.\d+\b", texto))   # ['10.0.0.5']

# Lookahead: extraer usuario antes de @ en un email
emails = "Contactar: admin@empresa.com o soporte@empresa.com"
usuarios = re.findall(r"[\w.]+(?=@)", emails)
print(usuarios)   # ['admin', 'soporte']

# Lookbehind: extraer el valor después de "puerto: "
log = "Evento: puerto: 443 activo, puerto: 8080 filtrado"
puertos = re.findall(r"(?<=puerto: )\d+", log)
print(puertos)   # ['443', '8080']
```

### Grupos de Captura

Los paréntesis `()` definen grupos de captura: partes del patrón cuyos contenidos se extraen de forma independiente de la coincidencia completa. Pueden nombrarse con la sintaxis `(?P<nombre>...)` para hacer el código más legible y mantenible.

```python
import re

# Grupos sin nombre: se acceden por índice
log_line = "2026-06-21 14:32:15 192.168.1.10 FAILED login root"
pattern = re.compile(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) ([\d.]+) (\w+) login (\w+)")
match = pattern.search(log_line)
if match:
    print(match.group(0))   # coincidencia completa
    print(match.group(1))   # 2026-06-21 (fecha)
    print(match.group(3))   # 192.168.1.10 (IP)
    print(match.groups())   # ('2026-06-21', '14:32:15', '192.168.1.10', 'FAILED', 'root')

# Grupos con nombre: se acceden por nombre
pattern_named = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) "
    r"(?P<ip>[\d.]+) (?P<status>\w+) login (?P<user>\w+)"
)
match = pattern_named.search(log_line)
if match:
    print(match.group("ip"))      # 192.168.1.10
    print(match.group("user"))    # root
    print(match.group("status"))  # FAILED
    print(match.groupdict())      # diccionario completo de todos los grupos
```

### Grupos de No Captura

En ocasiones se necesitan paréntesis para agrupar partes del patrón (por ejemplo, para aplicar un cuantificador sobre un conjunto de caracteres) sin que ello genere un grupo de captura. La sintaxis `(?:...)` crea un grupo de no captura, que agrupa sin extraer.

```python
import re

# Grupo de no captura: el (?:https?|ftp) agrupa la alternancia sin capturarla
urls = re.findall(r"(?:https?|ftp)://[\w./\-]+", "Visitar https://empresa.com o ftp://files.empresa.com")
print(urls)   # ['https://empresa.com', 'ftp://files.empresa.com']

# Con captura: el grupo adicional capturaría el protocolo por separado
urls_con_proto = re.findall(r"(https?|ftp)://([\w./\-]+)", "https://empresa.com")
print(urls_con_proto)   # [('https', 'empresa.com')]
```

### Alternancia

El operador `|` permite indicar que el patrón debe coincidir con una u otra alternativa.

```python
import re

log_status = "Resultado: FAILED en intento 1, SUCCESS en intento 4, FAILED en intento 5"
statuses = re.findall(r"FAILED|SUCCESS", log_status)
print(statuses)   # ['FAILED', 'SUCCESS', 'FAILED']
```

## Cadenas Crudas (_Raw Strings_)

Es una práctica esencial en Python escribir los patrones de expresiones regulares como **cadenas crudas** (_raw strings_), prefijando la cadena con `r`. Esto evita que Python interprete las barras invertidas del patrón (`\d`, `\n`, `\b`, etc.) como secuencias de escape de Python antes de que el motor de regex las procese.

```python
import re

texto = "IP: 192.168.1.10"

# Sin raw string: \d sería interpretado por Python como el carácter 'd' precedido de \
# (en la práctica muchas secuencias como \d no tienen significado en Python y se pasan
#  literalmente, pero \n, \t, \b sí son interpretadas, generando bugs difíciles de detectar)
print(re.findall("\d+", texto))    # funciona pero es mala práctica

# Con raw string: las barras invertidas se pasan literalmente al motor de regex
print(re.findall(r"\d+", texto))   # recomendado siempre
```

## Funciones Principales del Módulo `re`

### `re.search()`: Buscar en Cualquier Posición

`re.search(pattern, string, flags=0)` busca la primera coincidencia del patrón en cualquier posición de la cadena. Devuelve un objeto `Match` si encuentra una coincidencia, o `None` si no encuentra ninguna. A diferencia de `match()`, no requiere que la coincidencia esté al inicio de la cadena.

```python
import re

log_entry = "Jun 21 02:17:43 servidor sshd[1234]: Failed password for root from 203.0.113.5"

# search() encuentra la IP en cualquier posición de la cadena
match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", log_entry)
if match:
    print(f"IP encontrada: {match.group()}")        # 203.0.113.5
    print(f"Posición: {match.start()}–{match.end()}")

# Siempre verificar que match no sea None antes de usar .group()
resultado = re.search(r"CVE-\d{4}-\d+", "Esto no contiene ningún CVE")
if resultado is None:
    print("No se encontró ningún CVE en el texto")
```

### `re.match()`: Verificar el Inicio de la Cadena

`re.match(pattern, string, flags=0)` intenta hacer coincidir el patrón solo al **inicio** de la cadena. Si la coincidencia no puede comenzar desde el primer carácter, devuelve `None`. Esto lo hace especialmente adecuado para validar el formato completo de una cadena cuando se usa junto con el ancla `$` al final del patrón, o para verificar si una cadena comienza con un prefijo específico.

```python
import re

def is_valid_ip(ip):
    """Valida si una cadena tiene el formato correcto de una dirección IPv4."""
    pattern = r"^(25[0-5]|2[0-4]\d|[01]?\d\d?)(\.(25[0-5]|2[0-4]\d|[01]?\d\d?)){3}$"
    return bool(re.match(pattern, ip))

test_ips = ["192.168.1.10", "256.0.0.1", "10.0.0", "172.16.254.1", "abc.def.ghi.jkl"]
for ip in test_ips:
    valid = is_valid_ip(ip)
    print(f"  {'✅' if valid else '❌'} {ip}")

# Diferencia clave entre match() y search()
text = "Error: IP inválida 999.999.999.999"
print(re.match(r"\d+", text))    # None: la cadena no empieza con dígitos
print(re.search(r"\d+", text))   # Match: encuentra dígitos en alguna posición
```

### `re.fullmatch()`: Verificar la Cadena Completa

`re.fullmatch(pattern, string)` exige que el patrón coincida con la cadena **en su totalidad**, de principio a fin. Es equivalente a rodear el patrón con `^` y `$`, pero más explícito y menos propenso a errores. Es la función preferida cuando se quiere validar que una cadena completa tiene un formato específico.

```python
import re

def is_valid_cve(text):
    return bool(re.fullmatch(r"CVE-\d{4}-\d{4,7}", text, re.IGNORECASE))

test_cves = ["CVE-2020-1472", "cve-2021-41773", "CVE-20-123", "CVE-2023-23397-extra", "CVE-2024-1234567"]
for cve in test_cves:
    print(f"  {'✅' if is_valid_cve(cve) else '❌'} {cve}")
```

### `re.findall()`: Encontrar Todas las Coincidencias

`re.findall(pattern, string, flags=0)` devuelve una lista con todas las ocurrencias del patrón en la cadena, en orden de aparición. Si el patrón contiene grupos de captura, devuelve una lista de los contenidos de esos grupos (tuplas si hay más de un grupo).

```python
import re

nmap_output = """
Host: 192.168.1.10 Status: Up
22/tcp   open  ssh      OpenSSH 8.2
80/tcp   open  http     Apache 2.4.51
443/tcp  open  https    nginx 1.18
Host: 10.0.0.5 Status: Up
3389/tcp open  ms-wbt-server
"""

# Sin grupos: lista de coincidencias completas
ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", nmap_output)
print(f"IPs: {list(dict.fromkeys(ips))}")   # deduplicadas con dict

# Con un grupo: lista del contenido del grupo
ports = re.findall(r"(\d+)/tcp\s+open", nmap_output)
print(f"Puertos abiertos: {ports}")   # ['22', '80', '443', '3389']

# Con varios grupos: lista de tuplas
port_service = re.findall(r"(\d+)/tcp\s+open\s+(\S+)", nmap_output)
print(f"Puerto-servicio: {port_service}")   # [('22', 'ssh'), ('80', 'http'), ...]
```

### `re.finditer()`: Iterador de Objetos `Match`

`re.finditer(pattern, string, flags=0)` es similar a `findall()`, pero en lugar de devolver una lista de cadenas devuelve un **iterador de objetos `Match`**. Esto permite, para cada coincidencia, acceder no solo al texto coincidente, sino también a su posición en la cadena y al contenido de grupos individuales. Resulta más eficiente que `findall()` cuando se procesan cadenas muy largas, ya que no construye la lista completa en memoria antes de empezar a procesar.

```python
import re

log_data = """
2026-06-21 02:17:43 FAILED root 203.0.113.5
2026-06-21 02:17:51 FAILED admin 203.0.113.5
2026-06-21 02:18:03 FAILED root 185.220.101.5
2026-06-21 02:18:30 SUCCESS root 10.0.0.1
"""

pattern = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (FAILED|SUCCESS) (\w+) ([\d.]+)"
)

failed_attempts = {}
for match in pattern.finditer(log_data):
    timestamp, status, user, ip = match.groups()
    if status == "FAILED":
        # Contar intentos fallidos por IP
        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
        print(f"  [{timestamp}] Intento fallido: usuario '{user}' desde {ip}")

print(f"\nResumen de IPs atacantes:")
for ip, count in sorted(failed_attempts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {ip}: {count} intento(s) fallido(s)")
```

### `re.sub()`: Reemplazar Coincidencias

`re.sub(pattern, repl, string, count=0, flags=0)` reemplaza las coincidencias del patrón en la cadena por el valor de `repl`, que puede ser una cadena literal, una cadena con referencias a grupos de captura (`\1`, `\2`, o `\g<nombre>`), o una función que recibe el objeto `Match` y devuelve la cadena de reemplazo. El parámetro `count` limita el número de reemplazos (por defecto, se reemplazan todas las coincidencias).

```python
import re

# Reemplazo simple: redactar IPs de un log
log = "Conexión de 192.168.1.10 a 203.0.113.5 en el puerto 443"
redacted = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[REDACTED]", log)
print(redacted)
# Conexión de [REDACTED] a [REDACTED] en el puerto 443

# Reemplazo con grupos: reordenar componentes de una fecha
raw_dates = "Fecha de inicio: 21/06/2026 y fecha de fin: 30/06/2026"
iso_dates = re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", raw_dates)
print(iso_dates)
# Fecha de inicio: 2026-06-21 y fecha de fin: 2026-06-30

# Reemplazo con función: anonimizar usuarios de un log preservando estructura
auth_log = "FAILED login user:admin from 10.0.0.1 — FAILED login user:root from 10.0.0.2"

def anonymize_user(match):
    """Recibe el objeto Match y devuelve la cadena de reemplazo."""
    original_user = match.group(1)
    # Reemplaza por una versión hasheada (aquí simplificado)
    return f"user:[{'*' * len(original_user)}]"

anonymized = re.sub(r"user:(\w+)", anonymize_user, auth_log)
print(anonymized)

# Reemplazo con número limitado de ocurrencias
texto = "CVE CVE CVE"
print(re.sub(r"CVE", "VULN", texto, count=2))   # VULN VULN CVE
```

### `re.split()`: Dividir por un Patrón

`re.split(pattern, string, maxsplit=0, flags=0)` divide la cadena usando el patrón como separador, de forma análoga a `str.split()` pero con toda la potencia de las expresiones regulares para definir el separador. Si el patrón contiene grupos de captura, los contenidos de dichos grupos se incluyen en la lista resultante.

```python
import re

# Dividir por uno o más caracteres que no son alfanuméricos ni punto ni guion
raw_hostlist = "192.168.1.10, 10.0.0.5; 172.16.0.1 | 192.168.1.1\t10.10.10.5"
hosts = re.split(r"[,;\s|]+", raw_hostlist)
print(hosts)   # ['192.168.1.10', '10.0.0.5', '172.16.0.1', '192.168.1.1', '10.10.10.5']

# split() preservando los separadores con grupos de captura
linea = "Fecha=2026-06-21;Host=192.168.1.10;Puerto=443"
partes = re.split(r"(=|;)", linea)
print(partes)   # ['Fecha', '=', '2026-06-21', ';', 'Host', '=', '192.168.1.10', ';', 'Puerto', '=', '443']
```

## Compilación de Patrones con `re.compile()`

Cuando un mismo patrón se va a utilizar múltiples veces (por ejemplo, dentro de un bucle que procesa miles de líneas de un log), compilarlo previamente con `re.compile()` mejora el rendimiento, ya que el proceso de parseo y compilación del patrón solo se realiza una vez, en lugar de repetirse en cada llamada. El objeto compilado expone los mismos métodos que el módulo `re`, pero sin necesidad de pasar el patrón como argumento cada vez.

```python
import re

# Sin compile: el patrón se recompila en cada iteración
log_lines_raw = [
    "Jun 21 02:17:43 servidor sshd: Failed password for root from 203.0.113.5",
    "Jun 21 02:18:01 servidor sshd: Accepted password for admin from 10.0.0.1",
    "Jun 21 02:18:30 servidor sshd: Failed password for admin from 203.0.113.5",
]

# Con compile: el patrón se compila una sola vez
ssh_pattern = re.compile(
    r"(?P<time>\d{2}:\d{2}:\d{2}) \S+ sshd: (?P<status>Failed|Accepted) password for (?P<user>\w+) from (?P<ip>[\d.]+)"
)

for line in log_lines_raw:
    match = ssh_pattern.search(line)
    if match:
        d = match.groupdict()
        icon = "✅" if d["status"] == "Accepted" else "❌"
        print(f"  {icon} [{d['time']}] {d['status']} — usuario: {d['user']} — origen: {d['ip']}")
```

## Flags: Modificadores del Comportamiento

Las flags (o modificadores) alteran el modo en que el motor de expresiones regulares interpreta y aplica el patrón. Pueden pasarse como argumento `flags` en cualquiera de las funciones del módulo, o incluirse dentro del propio patrón usando la sintaxis `(?flags)`.

```python
import re

# re.IGNORECASE (re.I): ignorar diferencias de mayúsculas/minúsculas
texto = "El protocolo HTTP y también HTTPS son soportados"
print(re.findall(r"http", texto, re.IGNORECASE))   # ['HTTP', 'HTTP']

# re.MULTILINE (re.M): ^ y $ coinciden con el inicio/fin de cada LÍNEA
log_multilinea = "ERROR: fallo en conexión\nINFO: reintentando\nERROR: tiempo agotado"
print(re.findall(r"^ERROR.*", log_multilinea, re.MULTILINE))
# ['ERROR: fallo en conexión', 'ERROR: tiempo agotado']

# re.DOTALL (re.S): el punto (.) también coincide con el salto de línea
html_block = "<script>\nalert('xss')\n</script>"
match = re.search(r"<script>(.*?)</script>", html_block, re.DOTALL)
if match:
    print(f"Contenido del script: {match.group(1).strip()}")

# re.VERBOSE (re.X): permite escribir patrones con comentarios y espacios
ip_pattern = re.compile(r"""
    \b                          # frontera de palabra
    (                           # inicio del grupo principal
        (?:25[0-5]|             # 250-255
           2[0-4]\d|            # 200-249
           [01]?\d\d?)          # 0-199
        \.                      # punto literal
    ){3}                        # los tres primeros octetos
    (?:25[0-5]|2[0-4]\d|[01]?\d\d?)  # cuarto octeto
    \b                          # frontera de palabra
""", re.VERBOSE)

test = "IPs válidas: 192.168.1.10 y 10.0.0.5 — inválida: 999.999.0.1"
print(ip_pattern.findall(test))   # ['192.', '10.']  <- findall con grupo captura el último grupo

# Combinar múltiples flags con |
texto_multi = "Error\nerror\nERROR"
print(re.findall(r"^error$", texto_multi, re.IGNORECASE | re.MULTILINE))
# ['Error', 'error', 'ERROR']
```

## Patrones Comunes en Ciberseguridad

### Patrones de Validación

```python
import re

PATTERNS = {
    # Direcciones de red
    "IPv4"       : r"^(25[0-5]|2[0-4]\d|[01]?\d\d?)(\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)){3}$",
    "IPv6"       : r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$",
    "CIDR"       : r"^((?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?:\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)){3})/(\d|[12]\d|3[0-2])$",
    "Puerto"     : r"^([1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$",
    "MAC"        : r"^([0-9a-fA-F]{2}[:\-]){5}[0-9a-fA-F]{2}$",

    # Identificadores de seguridad
    "CVE"        : r"^CVE-\d{4}-\d{4,7}$",
    "MD5"        : r"^[a-fA-F0-9]{32}$",
    "SHA1"       : r"^[a-fA-F0-9]{40}$",
    "SHA256"     : r"^[a-fA-F0-9]{64}$",

    # Web y comunicaciones
    "Email"      : r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$",
    "URL"        : r"^https?://[^\s/$.?#].[^\s]*$",
    "Dominio"    : r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$",
}

test_cases = [
    ("IPv4",    "192.168.1.10"),
    ("IPv4",    "256.0.0.1"),
    ("CVE",     "CVE-2020-1472"),
    ("SHA256",  "d41d8cd98f00b204e9800998ecf8427e" * 2),
    ("MAC",     "AA:BB:CC:DD:EE:FF"),
    ("Email",   "admin@empresa.com"),
    ("CIDR",    "192.168.1.0/24"),
    ("Puerto",  "443"),
    ("Puerto",  "99999"),
]

for tipo, valor in test_cases:
    pattern = PATTERNS[tipo]
    valid = bool(re.fullmatch(pattern, valor, re.IGNORECASE))
    print(f"  {'✅' if valid else '❌'} {tipo:<10}: {valor}")
```

### Extracción de Datos de Logs

```python
import re

# Patrón para parsear una línea de /var/log/auth.log de Linux
AUTH_LOG_PATTERN = re.compile(
    r"(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"(?P<host>\S+)\s+sshd\[\d+\]:\s+(?P<status>Failed|Accepted|Disconnected)\s+"
    r"(?:password|publickey)\s+for\s+(?P<user>\S+)\s+from\s+(?P<ip>[\d.]+)"
)

auth_log_sample = """
Jun 21 02:17:43 servidor sshd[1234]: Failed password for root from 203.0.113.5
Jun 21 02:17:51 servidor sshd[1235]: Failed password for admin from 203.0.113.5
Jun 21 02:18:30 servidor sshd[1236]: Accepted password for svc_deploy from 10.0.0.1
Jun 21 02:19:01 servidor sshd[1237]: Failed password for root from 185.220.101.5
"""

# Conteo de intentos fallidos por IP
failed_by_ip = {}
for match in AUTH_LOG_PATTERN.finditer(auth_log_sample):
    d = match.groupdict()
    if d["status"] == "Failed":
        ip = d["ip"]
        failed_by_ip[ip] = failed_by_ip.get(ip, 0) + 1

print("Resumen de intentos fallidos SSH:")
for ip, count in sorted(failed_by_ip.items(), key=lambda x: x[1], reverse=True):
    alert = " ← POSIBLE BRUTE-FORCE" if count >= 2 else ""
    print(f"  {ip}: {count} intento(s){alert}")
```

## Buenas Prácticas

Siempre deben usarse cadenas crudas (`r"..."`) para los patrones de expresiones regulares, sin excepción, para evitar interferencias entre los caracteres de escape de Python y los metacaracteres de las regex. Cuando un mismo patrón se utilizará más de una o dos veces, debe compilarse con `re.compile()` para evitar la sobrecarga de recompilación en cada invocación.

Al verificar si una cadena completa se ajusta a un formato esperado, `re.fullmatch()` es preferible a `re.match()` con `$` al final, ya que comunica la intención con mayor claridad y es menos susceptible a omisiones accidentales del ancla final. En los grupos de captura, preferir los grupos con nombre (`(?P<nombre>...)`) sobre los grupos numerados cuando el número de grupos es mayor que dos o tres, ya que el código que referencia `match.group("ip")` es considerablemente más legible y mantenible que `match.group(3)`.

Finalmente, las expresiones regulares complejas deben documentarse siempre mediante la flag `re.VERBOSE`, que permite agregar comentarios inline al patrón, convirtiendo lo que podría ser una cadena opaca e incomprensible en un patrón bien documentado y fácil de mantener.
