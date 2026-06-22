# Entrada por Teclado y Salida por Pantalla en Python

## Introducción

La interacción con el usuario a través de la consola es uno de los mecanismos más fundamentales de cualquier programa que no sea completamente autónomo. En Python, esta interacción se canaliza principalmente a través de dos funciones incorporadas: `input()`, que permite leer texto introducido por el usuario desde el teclado, y `print()`, que permite mostrar información en la pantalla. Aunque ambas funciones pueden parecer simples en su uso más básico, esconden un conjunto considerable de opciones y matices que resultan esenciales para construir herramientas de línea de comandos bien pulidas, comunicativas y robustas, como las que se desarrollan habitualmente en el ámbito de la ciberseguridad.

## La Función `print()`

La función `print()` es el mecanismo principal de salida de datos en Python. Muestra en la consola los argumentos que recibe, convirtiéndolos automáticamente a cadena de texto si no lo son ya, y añadiendo por defecto un salto de línea al final. Sin embargo, su firma completa ofrece varios parámetros adicionales que permiten un control preciso sobre cómo y dónde se imprime la salida.

### Parámetros de `print()`

La firma completa de `print()` es la siguiente:

```python
print(*objetos, sep=' ', end='\n', file=sys.stdout, flush=False)
```

El parámetro `sep` define el separador que se inserta entre los objetos cuando se pasan varios argumentos en una sola llamada; por defecto es un espacio. El parámetro `end` define qué carácter se imprime al final; por defecto es un salto de línea (`\n`), pero puede cambiarse a cualquier otra cadena, o a una cadena vacía para evitar el salto de línea. El parámetro `file` permite redirigir la salida a cualquier objeto que tenga un método `write()`, como un archivo abierto en lugar de la consola. El parámetro `flush`, si es `True`, fuerza el vaciado inmediato del buffer de salida, útil en scripts de larga duración donde se quiere que la salida aparezca en tiempo real sin esperar a que el buffer se llene.

```python
# Uso básico: un solo argumento
print("Iniciando escaneo...")

# Múltiples argumentos: se separan con el separador por defecto (espacio)
print("Host:", "192.168.1.10", "Puerto:", 443)
# Host: 192.168.1.10 Puerto: 443

# Separador personalizado
print("192.168.1.10", 443, "https", sep=" | ")
# 192.168.1.10 | 443 | https

# Sin salto de línea al final (útil para construir líneas progresivamente)
print("Escaneando ", end="")
print("192.168.1.10", end="")
print("... ", end="")
print("hecho.")
# Escaneando 192.168.1.10... hecho.

# Redirigir la salida a un archivo
import sys
with open("/tmp/reporte.txt", "w") as archivo:
    print("Reporte de escaneo", file=archivo)
    print("Host: 192.168.1.10", file=archivo)

# flush=True: forzar salida inmediata durante un escaneo largo
import time
for i in range(1, 4):
    print(f"Probando host {i}/3...", flush=True)
    time.sleep(0.3)
```

### Carácteres de Escape

Dentro de las cadenas que se pasan a `print()`, Python reconoce una serie de secuencias de escape que representan caracteres especiales de control. Los más relevantes en el contexto de la salida por consola son los siguientes:

```python
print("Línea 1\nLínea 2\nLínea 3")   # \n: salto de línea
print("Columna1\tColumna2\tColumna3") # \t: tabulación horizontal
print("Barra invertida: \\")          # \\: imprime una sola barra invertida
print("Comillas: \"texto\"")          # \": comillas dobles dentro de una cadena con comillas dobles
print("\033[1;32m[+] Puerto abierto\033[0m")  # secuencias ANSI para color en terminal
```

Las secuencias de escape ANSI (`\033[código m`) merecen especial atención para el desarrollo de herramientas de consola en ciberseguridad, ya que permiten agregar color y formato al texto en terminales compatibles, mejorando considerablemente la legibilidad de la salida:

```python
# Códigos ANSI de color más comunes
RESET  = "\033[0m"
ROJO   = "\033[91m"
VERDE  = "\033[92m"
AMARILLO = "\033[93m"
AZUL   = "\033[94m"
NEGRITA = "\033[1m"

print(f"{VERDE}[+]{RESET} Puerto 443 abierto")
print(f"{ROJO}[-]{RESET} Conexión rechazada en el puerto 22")
print(f"{AMARILLO}[!]{RESET} Servicio identificado como vulnerable")
print(f"{NEGRITA}{AZUL}[*]{RESET} Iniciando enumeración DNS...")
```

## La Función `input()`

La función `input()` detiene la ejecución del programa, muestra opcionalmente un mensaje de prompt al usuario (el argumento que se le pasa), espera a que el usuario escriba algo y presione Enter, y devuelve todo lo que el usuario escribió como una **cadena de texto** (`str`). Este último punto es crítico: sin importar qué haya escrito el usuario (un número, una IP, un booleano), `input()` siempre devuelve una cadena, y es responsabilidad del programador convertir ese valor al tipo de dato necesario.

```python
# Uso básico: capturar texto del usuario
nombre = input("Ingresá tu nombre: ")
print(f"Hola, {nombre}")

# Capturar un número: se debe convertir explícitamente
try:
    puerto = int(input("Puerto a escanear: "))
    print(f"Escaneando el puerto {puerto}...")
except ValueError:
    print("Error: debés ingresar un número entero válido")
```

### Validación de la Entrada del Usuario

Uno de los principios más importantes al trabajar con `input()` es nunca confiar en que el usuario ingresará exactamente el tipo de dato esperado en el formato correcto. La validación de la entrada es una responsabilidad del programa, no del usuario. La forma más robusta de manejar esto es combinar `input()` con un bucle que siga pidiendo datos hasta que el usuario proporcione un valor válido, dando un mensaje de error claro en cada intento fallido.

```python
import ipaddress


def pedir_ip(prompt="IP objetivo: "):
    """Solicita al usuario una dirección IP válida, reintentando hasta obtenerla."""
    while True:
        entrada = input(prompt).strip()
        try:
            ip = ipaddress.ip_address(entrada)
            return str(ip)
        except ValueError:
            print(f"  [-] '{entrada}' no es una dirección IP válida. Intentá de nuevo.")


def pedir_entero(prompt, minimo=None, maximo=None):
    """Solicita un número entero, opcionalmente dentro de un rango."""
    while True:
        try:
            valor = int(input(prompt).strip())
            if minimo is not None and valor < minimo:
                print(f"  [-] El valor mínimo es {minimo}.")
            elif maximo is not None and valor > maximo:
                print(f"  [-] El valor máximo es {maximo}.")
            else:
                return valor
        except ValueError:
            print("  [-] Ingresá un número entero válido.")


def pedir_confirmacion(prompt="¿Confirmás? [s/n]: "):
    """Solicita una confirmación de sí o no al usuario."""
    while True:
        respuesta = input(prompt).strip().lower()
        if respuesta in ("s", "si", "sí", "y", "yes"):
            return True
        elif respuesta in ("n", "no"):
            return False
        else:
            print("  [-] Respondé 's' o 'n'.")


# Ejemplo de uso de las funciones de validación
ip = pedir_ip("IP objetivo: ")
puerto = pedir_entero("Puerto (1-65535): ", minimo=1, maximo=65535)
confirmado = pedir_confirmacion(f"¿Confirmás el escaneo de {ip}:{puerto}? [s/n]: ")

if confirmado:
    print(f"\n[*] Iniciando escaneo de {ip}:{puerto}...")
else:
    print("\n[!] Operación cancelada por el usuario.")
```

### Ocultar la Entrada: `getpass`

En situaciones donde el usuario debe ingresar una contraseña, una clave API u otro dato sensible, mostrar lo que escribe en pantalla representa un riesgo. El módulo `getpass` de la biblioteca estándar proporciona la función `getpass.getpass()`, que funciona de forma idéntica a `input()` pero oculta los caracteres que el usuario escribe, sin eco en la consola.

```python
import getpass

usuario = input("Usuario: ")
contrasena = getpass.getpass("Contraseña: ")   # lo que se escribe NO aparece en pantalla

print(f"Autenticando como '{usuario}'...")
```

## Formato de Texto y Presentación

La calidad de la salida por consola de una herramienta determina en gran medida la experiencia de quien la usa. Python ofrece herramientas avanzadas para alinear, justificar, truncar, separar con bordes y formatear números con precisión, todas directamente desde las f-strings o el método `format()`.

### Alineación y Ancho de Campo

Las f-strings permiten controlar el ancho mínimo de un campo y la alineación del texto dentro de él mediante la sintaxis `{valor:alineación ancho}`, donde `<` alinea a la izquierda, `>` a la derecha, y `^` centra el texto. Si el valor es más corto que el ancho especificado, se rellena con espacios (u otro carácter de relleno especificado antes del indicador de alineación).

```python
# Alineación en columnas para tablas de resultados
print(f"{'HOST':<20}{'PUERTO':<10}{'SERVICIO':<15}{'ESTADO'}")
print("-" * 55)
resultados = [
    ("192.168.1.10", 22, "ssh", "abierto"),
    ("192.168.1.10", 443, "https", "abierto"),
    ("192.168.1.11", 3389, "rdp", "filtrado"),
]
for host, puerto, servicio, estado in resultados:
    print(f"{host:<20}{puerto:<10}{servicio:<15}{estado}")
```

```
HOST                PUERTO    SERVICIO       ESTADO
-------------------------------------------------------
192.168.1.10        22        ssh            abierto
192.168.1.10        443       https          abierto
192.168.1.11        3389      rdp            filtrado
```

### Formateo de Números

Las f-strings también permiten controlar la presentación de valores numéricos: la cantidad de decimales a mostrar, el uso de separadores de miles, la notación científica, y la representación en distintas bases numéricas (hexadecimal, octal, binaria), esta última especialmente útil al trabajar con datos de red, hashes o representaciones de bytes.

```python
cvss = 9.81234
tiempo_respuesta = 0.004532
bytes_transferidos = 35876543

# Número de decimales
print(f"CVSS: {cvss:.1f}")                # 9.8  (1 decimal)
print(f"Tiempo: {tiempo_respuesta:.4f}s") # 0.0045 (4 decimales)

# Separadores de miles
print(f"Bytes: {bytes_transferidos:,}")    # 35,876,543
print(f"Bytes: {bytes_transferidos:,}".replace(",", "."))  # 35.876.543

# Representaciones en distintas bases (útil para datos de red)
ip_raw = 0xC0A8010A   # 192.168.1.10 en hexadecimal
print(f"Hex: {ip_raw:#010x}")   # 0xc0a8010a
print(f"Dec: {ip_raw}")          # 3232235786
print(f"Bin: {ip_raw:#034b}")    # representación binaria con prefijo 0b

byte_valor = 255
print(f"Hex: {byte_valor:02x}")   # ff  (hexadecimal, 2 dígitos con relleno 0)
print(f"Bin: {byte_valor:08b}")   # 11111111 (binario, 8 bits con relleno 0)
```

### Texto Centrado y Bordes para Encabezados

El método `str.center()` centra una cadena dentro de un ancho específico, rellenando con un carácter a elegir a ambos lados. Combinado con líneas de separación, permite construir encabezados de sección limpios y bien estructurados para la salida de herramientas de consola.

```python
ANCHO = 60

def titulo(texto):
    print("\n" + "═" * ANCHO)
    print(texto.center(ANCHO))
    print("═" * ANCHO)

def subtitulo(texto):
    print(f"\n  ── {texto} {'─' * (ANCHO - len(texto) - 6)}")

titulo("REPORTE DE RECONOCIMIENTO")
subtitulo("Hosts activos detectados")
```

### Cadenas Multilínea y `textwrap`

Cuando la salida incluye texto largo que debe presentarse dentro de un ancho determinado (como descripciones de vulnerabilidades o mensajes de ayuda), el módulo `textwrap` de la biblioteca estándar proporciona herramientas para envolver y sangrar texto automáticamente.

```python
import textwrap

descripcion_vuln = (
    "MS17-010 (EternalBlue): vulnerabilidad crítica en el protocolo SMBv1 de Windows "
    "que permite la ejecución remota de código sin autenticación. Fue explotada masivamente "
    "por el ransomware WannaCry en 2017 y sigue siendo relevante en redes con sistemas sin parchear."
)

print(textwrap.fill(descripcion_vuln, width=60))
print()
# textwrap.indent agrega sangría a cada línea de un bloque de texto
print(textwrap.indent(descripcion_vuln, prefix="    "))
```

## Codificación de Caracteres

La codificación de caracteres define la forma en que los caracteres de texto se representan como bytes en la memoria y en el almacenamiento. En el contexto de la entrada y salida por consola, la codificación es relevante porque distintos sistemas operativos, terminales y configuraciones regionales pueden usar distintas codificaciones por defecto, lo que puede provocar que caracteres no ASCII (como las vocales acentuadas, la ñ, o caracteres de otros alfabetos) se muestren de forma incorrecta o provoquen errores.

### Unicode y UTF-8

Desde Python 3, todas las cadenas de texto (`str`) son Unicode internamente, lo que significa que pueden representar cualquier carácter de cualquier idioma sin limitaciones. El problema de la codificación surge en el momento en que ese texto se convierte en bytes para ser almacenado o transmitido, y de nuevo al convertirlo de bytes a texto para mostrarlo.

**UTF-8** es la codificación más ampliamente adoptada en la actualidad: es compatible con ASCII para los caracteres del inglés básico (los primeros 128 caracteres), y extiende ese rango para representar cualquier carácter Unicode usando entre 1 y 4 bytes según el carácter. Python 3 usa UTF-8 como codificación por defecto para la mayoría de las operaciones de entrada/salida.

```python
import sys

# Verificar la codificación que usa el intérprete para stdin/stdout
print(f"Codificación de stdout: {sys.stdout.encoding}")
print(f"Codificación de stdin:  {sys.stdin.encoding}")
print(f"Codificación del sistema: {sys.getdefaultencoding()}")
```

### Codificación y Decodificación Manual

Cuando se trabaja con datos binarios (sockets de red, archivos en formatos específicos, hashes), es necesario convertir manualmente entre cadenas de texto y bytes. En Python, `str.encode()` convierte una cadena de texto a bytes usando la codificación especificada, y `bytes.decode()` realiza la operación inversa.

```python
# Codificación: str -> bytes
mensaje = "Payload: ñoño"
mensaje_bytes = mensaje.encode("utf-8")
print(type(mensaje_bytes), mensaje_bytes)

# Decodificación: bytes -> str
mensaje_recuperado = mensaje_bytes.decode("utf-8")
print(tipo_recuperado := type(mensaje_recuperado), mensaje_recuperado)

# Manejo de errores de decodificación: qué hacer si hay bytes inválidos
datos_corruptos = b"Respuesta del servidor: \xff\xfe datos"
texto_seguro = datos_corruptos.decode("utf-8", errors="replace")  # reemplaza bytes inválidos con ?
texto_ignorado = datos_corruptos.decode("utf-8", errors="ignore")  # descarta bytes inválidos
print(texto_seguro)
print(texto_ignorado)
```

Los parámetros de manejo de errores en `decode()` resultan especialmente relevantes en ciberseguridad al procesar respuestas de servidores o datos de red que pueden contener bytes fuera del rango UTF-8, como ocurre al interactuar con servicios que devuelven texto en codificaciones antiguas (Latin-1, Windows-1252) o con datos binarios mezclados con texto.

### Configuración de la Codificación al Abrir Archivos

Al abrir archivos de texto con `open()`, siempre conviene especificar explícitamente la codificación mediante el parámetro `encoding`, en lugar de depender de la codificación por defecto del sistema, que puede variar entre plataformas.

```python
# Escritura y lectura con codificación explícita
with open("reporte.txt", "w", encoding="utf-8") as f:
    f.write("Hallazgo: vulnerabilidad crítica en 192.168.1.10\n")
    f.write("CVE: CVE-2020-1472 — ZeroLogon\n")

with open("reporte.txt", "r", encoding="utf-8") as f:
    contenido = f.read()
    print(contenido)
```

## Gestión de la Salida Estándar y de Error

Python diferencia entre dos flujos de salida independientes: `sys.stdout` (salida estándar, donde va todo lo que imprime `print()`) y `sys.stderr` (salida de error estándar, destinada a mensajes de diagnóstico y error). Esta distinción resulta importante en el desarrollo de herramientas de línea de comandos porque permite al usuario final separar la salida "útil" del programa (resultados, datos) de los mensajes de error o advertencia, por ejemplo redirigiendo `stdout` a un archivo mientras los errores siguen apareciendo en la terminal.

```python
import sys

def log_info(mensaje):
    print(f"[*] {mensaje}", file=sys.stdout)

def log_ok(mensaje):
    print(f"[+] {mensaje}", file=sys.stdout)

def log_error(mensaje):
    # Los errores van a stderr: se separan de la salida normal
    print(f"[-] {mensaje}", file=sys.stderr)

def log_warn(mensaje):
    print(f"[!] {mensaje}", file=sys.stderr)

log_info("Iniciando escaneo de 192.168.1.0/24")
log_ok("Host 192.168.1.10 activo")
log_warn("Puerto 23 (Telnet) abierto: protocolo inseguro")
log_error("No se pudo resolver el hostname 'objetivo.local'")
```

Al ejecutar este script desde la terminal, es posible redirigir stdout y stderr de forma independiente:

```bash
# Solo muestra en pantalla los errores; los resultados se guardan en el archivo
python3 scanner.py > resultados.txt

# Redirige los errores a un archivo de log separado
python3 scanner.py > resultados.txt 2> errores.log

# Descarta los errores completamente
python3 scanner.py 2>/dev/null
```

## Buenas Prácticas

Al diseñar la interacción con el usuario en una herramienta de consola, conviene mantener los mensajes de prompt de `input()` claros e indicativos del formato esperado, especificando entre corchetes o paréntesis el formato o los valores válidos cuando no son obvios (por ejemplo, `"Puerto [1-65535]: "` o `"Protocolo [tcp/udp]: "`). Toda entrada del usuario debe validarse antes de utilizarse, especialmente en herramientas de seguridad donde una entrada malformada podría causar un comportamiento inesperado.

Para la salida, conviene separar los mensajes de estado y error de los resultados enviando los primeros a `sys.stderr` y los segundos a `sys.stdout`, lo que permite que la herramienta se integre correctamente en pipelines de shell. Especificar siempre `encoding="utf-8"` al abrir archivos de texto y usar `errors="replace"` o `errors="ignore"` al decodificar datos de red de origen desconocido son prácticas defensivas que evitan excepciones inesperadas en entornos con configuraciones regionales distintas. Finalmente, usar `getpass.getpass()` en lugar de `input()` siempre que se soliciten contraseñas u otros datos sensibles es una medida básica de seguridad que no debería omitirse nunca.