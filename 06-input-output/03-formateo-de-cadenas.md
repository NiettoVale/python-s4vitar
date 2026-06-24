# Formateo de Cadenas y Manipulación de Texto en Python

## Introducción

Las cadenas de texto son el tipo de dato más omnipresente en cualquier herramienta de software real. En ciberseguridad en particular, prácticamente todas las operaciones que importan implican manipular texto: parsear la salida de `nmap` o `gobuster`, construir payloads, normalizar nombres de usuario, verificar si un CVE está presente en un reporte, dividir una línea de `/etc/passwd` en sus campos, generar mensajes de log con variables interpoladas. Dominar el formateo y la manipulación de cadenas en Python es, por lo tanto, una habilidad que se usa en cada script que se escribe.

## Formateo de Cadenas

Python ha evolucionado a lo largo del tiempo en cuanto a las formas disponibles para interpolar variables dentro de cadenas de texto. Actualmente conviven tres métodos distintos, cada uno heredado de una época diferente del lenguaje.

### Operador `%`: Formateo Clásico

El operador `%` es el mecanismo de formateo más antiguo de Python, heredado de la sintaxis `printf` del lenguaje C. Funciona colocando marcadores de posición tipados dentro de la cadena (`%s` para cadenas, `%d` para enteros, `%f` para flotantes) y proporcionando los valores a insertar como una tupla a la derecha del operador.

```python
host = "192.168.1.10"
port = 443
response_time = 0.045

print("Host: %s — Puerto: %d — Tiempo: %.3f seg" % (host, port, response_time))
# Host: 192.168.1.10 — Puerto: 443 — Tiempo: 0.045 seg

# Control de ancho mínimo y alineación con %
print("%-20s %5d" % ("192.168.1.10", 22))    # izquierda, derecha
print("%-20s %5d" % ("192.168.1.11", 3389))
```

Si bien el operador `%` sigue siendo válido y puede encontrarse en código heredado con frecuencia, se considera desaconsejado para código nuevo, ya que los métodos más modernos son más legibles y menos propensos a errores cuando se trabaja con muchas variables.

### Método `format()`: Formateo Versátil

Introducido en Python 2.6, el método `format()` utiliza llaves `{}` como marcadores de posición y ofrece mayor flexibilidad que el operador `%`. Los marcadores pueden dejarse vacíos (los valores se asignan en orden), contener un índice posicional, o contener un nombre explícito para mayor claridad. Dentro de las llaves puede especificarse un formato de salida complejo después de dos puntos.

```python
# Posicional implícito (en orden)
print("Host: {} — Puerto: {}".format("192.168.1.10", 443))

# Posicional explícito (por índice)
print("{0} escaneando {1}:{2}".format("nmap", "192.168.1.10", 443))

# Por nombre (mayor legibilidad)
print("{tool} encontró {count} puertos abiertos en {host}".format(
    tool="masscan",
    count=3,
    host="192.168.1.10",
))

# Alineación y ancho
print("{:<20}{:>10}".format("192.168.1.10", 443))     # izquierda / derecha
print("{:^30}".format("REPORTE DE ESCANEO"))           # centrado
print("{:*^30}".format(" REPORTE "))                   # centrado con relleno de *

# Separador de miles y decimales
print("{:,}".format(35_876_543))              # 35,876,543
print("{:,.2f}".format(9876543.21))           # 9,876,543.21
print("{:,}".format(35_876_543).replace(",", "."))  # 35.876.543 (formato regional)
```

### F-Strings: El Estándar Actual

Las f-strings, disponibles desde Python 3.6, son la forma más concisa, legible y actualmente recomendada para interpolar variables y expresiones dentro de cadenas. Se definen anteponiendo la letra `f` (o `F`) antes de la comilla de apertura, y permiten insertar cualquier expresión Python válida directamente dentro de llaves `{}`.

```python
host = "192.168.1.10"
port = 443
service = "https"
cvss = 9.8

# Interpolación básica
print(f"Host: {host} — Puerto: {port} — Servicio: {service}")

# Expresiones directamente dentro de las llaves
ports = [22, 80, 443, 3389]
print(f"Puertos detectados: {len(ports)} — Primero: {ports[0]}")

# Llamadas a métodos
print(f"Host en mayúsculas: {host.upper()}")
print(f"Puerto formateado: {port:05d}")         # 00443 (relleno con ceros)
print(f"CVSS: {cvss:.1f}")                      # 9.8 (1 decimal)
print(f"Hex del puerto: {port:#06x}")            # 0x01bb

# Multilinea (f-string con triple comilla)
reporte = f"""
=== Hallazgo ===
Host    : {host}
Puerto  : {port}
Servicio: {service}
CVSS    : {cvss}
"""
print(reporte)

# Depuración con el especificador = (Python 3.8+)
# Imprime automáticamente "nombre_variable=valor"
print(f"{host=}")    # host='192.168.1.10'
print(f"{cvss=}")    # cvss=9.8
```

---

## Métodos de Manipulación de Cadenas

Python incluye una extensa colección de métodos de cadena que cubren prácticamente cualquier operación de manipulación de texto que se pueda necesitar. Todos estos métodos operan sobre la cadena original y **devuelven una nueva cadena** con el resultado, sin modificar la original (recordar que las cadenas son inmutables en Python).

---

### `strip()`, `lstrip()`, `rstrip()`: Eliminar Espacios y Caracteres

El método `strip()` elimina los espacios en blanco (y el carácter `\n`, `\t`, etc.) del inicio y del final de la cadena. `lstrip()` solo elimina del lado izquierdo, y `rstrip()` solo del derecho. Opcionalmente, puede pasarse un argumento con los caracteres específicos a eliminar (no necesariamente espacios).

```python
linea_log = "   [INFO] Escaneo finalizado   \n"

print(repr(linea_log.strip()))     # '[INFO] Escaneo finalizado'
print(repr(linea_log.lstrip()))    # '[INFO] Escaneo finalizado   \n'
print(repr(linea_log.rstrip()))    # '   [INFO] Escaneo finalizado'

# Con argumento: eliminar caracteres específicos
cve = "---CVE-2020-1472---"
print(cve.strip("-"))    # 'CVE-2020-1472'

# Caso de uso típico: limpiar líneas al leer un archivo
with open("/etc/hosts", "r") as f:
    hosts_clean = [line.strip() for line in f if line.strip() and not line.startswith("#")]
```

---

### `lower()` y `upper()`: Cambio de Caso

`lower()` convierte todos los caracteres alfabéticos de la cadena a minúsculas, y `upper()` los convierte a mayúsculas. Son operaciones fundamentales para normalizar datos antes de compararlos o almacenarlos, ya que evitan que "Admin", "ADMIN" y "admin" sean tratados como valores distintos.

```python
username = "ADMIN"
protocol = "HTTPS"

print(username.lower())   # admin
print(protocol.lower())   # https

# Normalización antes de comparar
input_user = "ROOT"
if input_user.lower() == "root":
    print("Usuario root detectado")

# Generar headers HTTP normalizados
header = "content-type"
print(header.upper())    # CONTENT-TYPE
```

---

### `capitalize()` y `swapcase()`: Transformaciones de Caso Adicionales

`capitalize()` convierte el primer carácter de la cadena a mayúscula y todos los demás a minúscula. `swapcase()` invierte el caso de cada carácter: los que estaban en mayúscula pasan a minúscula y viceversa. Este último tiene usos específicos en técnicas de *case mutation* para evasión de filtros.

```python
service = "openssh"
print(service.capitalize())    # Openssh

title = "reporte de reconocimiento"
print(title.capitalize())      # Reporte de reconocimiento

# swapcase: inversión de caso carácter a carácter
payload = "alert(document.cookie)"
print(payload.swapcase())     # ALERT(DOCUMENT.COOKIE)

# Caso de uso en ciberseguridad: generación de variantes de payload para evasión
original = "SELECT * FROM users"
print(original.swapcase())    # select * FROM USERS
```

---

### `replace()`: Reemplazo de Subcadenas

El método `replace(old, new, count=-1)` devuelve una nueva cadena donde todas las ocurrencias de `old` han sido reemplazadas por `new`. El parámetro opcional `count` limita el número máximo de reemplazos.

```python
log_line = "192.168.1.10 192.168.1.10 CONNECTED 192.168.1.10"

# Reemplazar todas las ocurrencias
print(log_line.replace("192.168.1.10", "[REDACTED]"))
# [REDACTED] [REDACTED] CONNECTED [REDACTED]

# Reemplazar solo la primera ocurrencia
print(log_line.replace("192.168.1.10", "[REDACTED]", 1))
# [REDACTED] 192.168.1.10 CONNECTED 192.168.1.10

# Sanitizar salida antes de incluir en un reporte
sensitive_output = "password: S3cr3t! api_key: ABCDEF123"
safe_output = sensitive_output.replace("S3cr3t!", "***").replace("ABCDEF123", "***")
print(safe_output)

# Normalizar separadores de miles en números formateados
number = "{:,}".format(1_234_567)
print(number.replace(",", "."))    # 1.234.567
```

---

### `split()` y `join()`: Dividir y Unir

`split(sep=None, maxsplit=-1)` divide la cadena en una lista de subcadenas usando el separador indicado. Si no se indica separador, divide por cualquier secuencia de espacios en blanco y descarta los elementos vacíos. `maxsplit` limita la cantidad máxima de divisiones. `join(iterable)` es la operación inversa: une todos los elementos de un iterable en una sola cadena, usando la cadena sobre la que se invoca como separador entre ellos.

```python
# split(): dividir una cadena en partes
line_passwd = "root:x:0:0:root:/root:/bin/bash"
fields = line_passwd.split(":")
print(fields)
# ['root', 'x', '0', '0', 'root', '/root', '/bin/bash']

username = fields[0]
uid      = fields[2]
shell    = fields[6]
print(f"Usuario: {username} | UID: {uid} | Shell: {shell}")

# maxsplit: limitar el número de divisiones
log_entry = "2026-06-21 14:32:01 INFO Puerto 443 abierto en 192.168.1.10"
timestamp, level, *message_parts = log_entry.split(" ", maxsplit=2)
message = message_parts[0] if message_parts else ""
print(f"Timestamp: {timestamp} {level} | Mensaje: {message}")

# split() sin argumento: divide por espacios/tabs/newlines
raw_hosts = "  192.168.1.10   192.168.1.11   10.0.0.5  "
hosts = raw_hosts.split()
print(hosts)   # ['192.168.1.10', '192.168.1.11', '10.0.0.5']

# join(): unir elementos de una lista en una cadena
ports = [22, 80, 443, 8080]
print(",".join(str(p) for p in ports))    # 22,80,443,8080
print(" | ".join(str(p) for p in ports)) # 22 | 80 | 443 | 8080
print("\n".join(hosts))                   # cada host en una línea

# join() para reconstruir una línea modificada de /etc/passwd
fields[6] = "/bin/sh"   # cambiar el shell
reconstructed = ":".join(fields)
print(reconstructed)    # root:x:0:0:root:/root:/bin/sh
```

---

### `startswith()` y `endswith()`: Verificar Prefijo y Sufijo

Ambos métodos devuelven `True` si la cadena comienza (`startswith`) o termina (`endswith`) con la subcadena (o tupla de subcadenas) especificada. Admiten parámetros opcionales de inicio y fin para limitar la búsqueda a una porción de la cadena.

```python
url = "https://192.168.1.10/admin/panel"
filename = "malware_sample.exe"
log = "# Este es un comentario"

# Verificaciones individuales
print(url.startswith("https"))      # True
print(url.startswith("http"))       # True  (https empieza con http también)
print(url.endswith("/admin/panel")) # True
print(filename.endswith(".exe"))    # True

# Tupla de opciones: devuelve True si coincide con alguna
extensions_executable = (".exe", ".dll", ".bat", ".ps1", ".sh")
print(filename.endswith(extensions_executable))   # True

# Filtrar líneas de un archivo ignorando comentarios y vacías
lines = [
    "# Comentario",
    "192.168.1.10",
    "",
    "# Otro comentario",
    "10.0.0.5",
]
clean_lines = [l for l in lines if l and not l.startswith("#")]
print(clean_lines)    # ['192.168.1.10', '10.0.0.5']

# Clasificar URLs por protocolo
urls = ["https://empresa.com", "http://old.empresa.com", "ftp://files.empresa.com"]
for u in urls:
    if u.startswith("http://"):
        print(f"[!] URL insegura detectada: {u}")
    elif u.startswith("https://"):
        print(f"[+] URL segura: {u}")
    else:
        print(f"[*] Protocolo no estándar: {u}")
```

---

### `find()` e `index()`: Búsqueda de Subcadenas

Ambos métodos buscan una subcadena dentro de la cadena y devuelven el índice de la primera ocurrencia. La diferencia crítica es el comportamiento cuando la subcadena no se encuentra: `find()` devuelve `-1`, mientras que `index()` lanza una excepción `ValueError`. Esta diferencia determina cuándo usar uno u otro: `find()` cuando la ausencia de la subcadena es un escenario normal que debe manejarse con una condición, `index()` cuando la ausencia representa un error real que debe interrumpir el flujo.

```python
response_header = "HTTP/1.1 200 OK\r\nServer: Apache/2.4.51\r\nContent-Type: text/html"

# find(): devuelve -1 si no encuentra la subcadena
server_pos = response_header.find("Server:")
if server_pos != -1:
    print(f"Cabecera 'Server' encontrada en la posición {server_pos}")
else:
    print("Cabecera 'Server' no presente")

# find() con inicio y fin opcionales
vuln_header = response_header.find("Apache", server_pos)
print(f"Versión de Apache desde posición: {vuln_header}")

# index(): lanza ValueError si no encuentra la subcadena
try:
    pos = response_header.index("X-Powered-By")
except ValueError:
    print("Cabecera 'X-Powered-By' no encontrada (puede ser una buena práctica de seguridad)")

# rfind(): busca desde el final de la cadena
path = "/var/www/html/uploads/shell.php"
last_slash = path.rfind("/")
filename_only = path[last_slash + 1:]
print(f"Nombre del archivo: {filename_only}")    # shell.php
```

---

### `count()`: Contar Ocurrencias

El método `count(sub, start=0, end=len(string))` devuelve el número de veces que la subcadena `sub` aparece de forma no solapada en la cadena. Admite parámetros opcionales de inicio y fin para limitar la búsqueda.

```python
log_content = """
192.168.1.10 FAILED login
192.168.1.10 FAILED login
192.168.1.10 FAILED login
192.168.1.20 SUCCESS login
192.168.1.10 FAILED login
"""

failed_attempts = log_content.count("FAILED")
success_count   = log_content.count("SUCCESS")
ip_occurrences  = log_content.count("192.168.1.10")

print(f"Intentos fallidos: {failed_attempts}")       # 4
print(f"Accesos exitosos: {success_count}")          # 1
print(f"Apariciones de .10: {ip_occurrences}")       # 4

# count() de un carácter específico en un payload
payload = "<script>alert('xss')</script>"
angle_brackets = payload.count("<")
print(f"Cantidad de '<' en el payload: {angle_brackets}")    # 2
```

---

### Métodos `is*`: Verificación del Contenido

Python ofrece una familia de métodos que permiten verificar el tipo o composición del contenido de una cadena, devolviendo siempre un booleano. Son útiles para validar entradas antes de procesarlas.

```python
# isdigit(): True si todos los caracteres son dígitos (0-9)
print("443".isdigit())        # True
print("443a".isdigit())       # False
print("".isdigit())           # False (cadena vacía devuelve False)

# isalpha(): True si todos los caracteres son letras (sin espacios, dígitos ni símbolos)
print("admin".isalpha())      # True
print("admin123".isalpha())   # False

# isalnum(): True si todos los caracteres son letras o dígitos
print("admin123".isalnum())   # True
print("admin_123".isalnum())  # False (guion bajo no es alfanumérico)

# islower() / isupper(): verificar si todos los caracteres con case son minúsculas/mayúsculas
print("admin".islower())      # True
print("ADMIN".isupper())      # True
print("Admin".islower())      # False

# istitle(): True si la cadena está en formato Título (cada palabra empieza con mayúscula)
print("Cross Site Scripting".istitle())   # True
print("cross site scripting".istitle())   # False

# isspace(): True si todos los caracteres son espacios en blanco
print("   ".isspace())        # True
print("  a ".isspace())       # False

# Casos de uso reales en validación de entrada
def validate_port(value):
    """Valida que el valor sea una cadena de dígitos representando un puerto válido."""
    if not value.isdigit():
        return False, "El puerto debe ser numérico"
    port = int(value)
    if not (1 <= port <= 65535):
        return False, "El puerto debe estar entre 1 y 65535"
    return True, port

ok, result = validate_port("443")
print(f"Puerto válido: {result}")

ok, result = validate_port("abc")
print(f"Puerto inválido: {result}")
```

---

### Operadores `in` y `not in`: Pertenencia en Cadenas

Los operadores `in` y `not in` verifican si una subcadena está contenida dentro de otra cadena, devolviendo un booleano. Son más directos y legibles que `find()` cuando solo se necesita saber si la subcadena existe, sin importar su posición.

```python
user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1)"
headers_raw = "X-Forwarded-For: 10.0.0.1\nAuthorization: Bearer abc123"

# in: verificación de pertenencia
print("Googlebot" in user_agent)       # True
print("Authorization" in headers_raw)  # True
print("Cookie" not in headers_raw)     # True

# Detectar keywords sospechosos en una URL
suspicious_url = "https://empresa.com/page?id=1 OR 1=1 --"
sql_keywords = ["OR 1=1", "UNION SELECT", "DROP TABLE", "--", "/*"]
detected = [kw for kw in sql_keywords if kw in suspicious_url]
if detected:
    print(f"[!] Posible SQLi detectado. Keywords: {detected}")
```

---

### `maketrans()` y `translate()`: Traducción Carácter a Carácter

`str.maketrans(x, y, z)` construye una **tabla de traducción**: un diccionario que mapea el ordinal Unicode de cada carácter en `x` al carácter correspondiente en `y`, y opcionalmente elimina los caracteres en `z`. `translate(table)` aplica esa tabla de traducción a la cadena, reemplazando o eliminando caracteres de forma eficiente. Juntos, forman el mecanismo más eficiente para realizar sustituciones carácter a carácter en Python, más rápido que múltiples llamadas a `replace()`.

```python
# Caso de uso clásico: cifrado ROT13 (sustitución simple)
plain = "abcdefghijklmnopqrstuvwxyz"
rot13 = "nopqrstuvwxyzabcdefghijklm"
table_rot13 = str.maketrans(plain + plain.upper(), rot13 + rot13.upper())

message = "AttackAtDawn"
encrypted = message.translate(table_rot13)
decrypted = encrypted.translate(table_rot13)   # ROT13 es su propio inverso

print(f"Original : {message}")     # AttackAtDawn
print(f"Cifrado  : {encrypted}")   # NggnapxNgQnja
print(f"Descifrado: {decrypted}")  # AttackAtDawn

# Eliminar caracteres no deseados (tercer argumento de maketrans)
# El tercer argumento especifica caracteres a ELIMINAR completamente
payload_raw = "  <script>  alert( 1 )  </script>  "
table_remove = str.maketrans("", "", " <>/()")   # eliminar espacios y símbolos
sanitized = payload_raw.translate(table_remove)
print(f"Sanitizado: {sanitized}")   # scriptalert1/script

# Normalizar caracteres similares (útil para comparación de usernames o evasión)
lookalikes = str.maketrans("0O1lI", "oolis")   # sustituir confusables
username_raw = "Adm1n0fSyst3m"
normalized = username_raw.translate(lookalikes)
print(f"Normalizado: {normalized}")
```

---

### `istitle()` y `capitalize()`: Formato de Título

`istitle()` verifica si la cadena sigue el formato Título (cada palabra comienza con mayúscula y el resto es minúscula), mientras que `capitalize()` convierte únicamente el primer carácter a mayúscula y todos los demás a minúscula.

```python
vuln_name = "cross site scripting"
print(vuln_name.capitalize())                      # Cross site scripting
print(vuln_name.title())                           # Cross Site Scripting
print("Cross Site Scripting".istitle())            # True
print("Cross site scripting".istitle())            # False

# title() para formatear nombres de vulnerabilidades
vuln_list = ["sql injection", "path traversal", "command injection"]
formatted = [v.title() for v in vuln_list]
print(formatted)   # ['Sql Injection', 'Path Traversal', 'Command Injection']
```

---

## Métodos de Expresiones Regulares: el Módulo `re`

Para búsquedas y reemplazos que van más allá de subcadenas literales, Python ofrece el módulo `re`, que permite definir **patrones** mediante expresiones regulares. Las funciones más relevantes son `re.search()` (busca el patrón en cualquier posición de la cadena), `re.match()` (solo verifica el inicio de la cadena), `re.findall()` (devuelve todas las coincidencias), `re.sub()` (reemplaza coincidencias) y `re.compile()` (precompila un patrón para reutilizarlo eficientemente).

```python
import re

nmap_output = """
Host: 192.168.1.10 Status: Up
Port 22/tcp: ssh OpenSSH 8.2
Port 80/tcp: http Apache 2.4.51
Port 443/tcp: https nginx 1.18
Host: 10.0.0.5 Status: Up
Port 3389/tcp: ms-wbt-server
"""

# Extraer todas las IPs del output con findall()
ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", nmap_output)
print(f"IPs detectadas: {ips}")

# Extraer puertos abiertos con grupos de captura
ports_found = re.findall(r"Port (\d+)/tcp: (\w+)", nmap_output)
for port, service in ports_found:
    print(f"  Puerto {port} → {service}")

# Redactar IPs en un log (sub para reemplazar)
redacted = re.sub(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "[REDACTED]", nmap_output)
print(redacted[:60])   # primeras 60 chars para no llenar la pantalla

# Validar formato de CVE con search()
def is_valid_cve(text):
    """Verifica si una cadena sigue el formato estándar CVE-AAAA-NNNNN."""
    return bool(re.search(r"CVE-\d{4}-\d{4,7}", text, re.IGNORECASE))

print(is_valid_cve("CVE-2020-1472"))     # True
print(is_valid_cve("cve-2021-41773"))   # True  (IGNORECASE)
print(is_valid_cve("CVE-20-123"))        # False
```

---

## Buenas Prácticas

Para la interpolación de variables en cadenas, los f-strings son la opción por defecto en cualquier código Python 3.6+: son más legibles, más rápidos que `format()` y más seguros que el operador `%`. El operador `%` debe reservarse para código que deba mantener compatibilidad con versiones antiguas del lenguaje, y `format()` para los casos donde se necesita una plantilla reutilizable separada de los datos.

Al manipular texto proveniente de fuentes externas (archivos, input del usuario, respuestas de red), siempre conviene aplicar `strip()` antes de cualquier comparación para evitar que espacios o saltos de línea invisibles generen falsos negativos. Para comparaciones de cadenas de texto que representan identificadores (usuarios, dominios, protocolos), normalizar a minúsculas con `lower()` antes de comparar es una práctica que evita una clase frecuente de errores. Finalmente, cuando se necesita verificar simplemente si una subcadena existe en otra cadena, preferir `in` sobre `find()` resulta más legible; reservar `find()` para cuando además se necesita la posición, e `index()` solo cuando la ausencia de la subcadena representa un error genuino que debe propagarse.