# Manejo de Errores y Excepciones en Python

## Introducción al Manejo de Errores

Los errores son inevitables en la programación: pueden originarse por fallos en la lógica del propio código, por datos de entrada incorrectos o inesperados, por problemas de conectividad de red, por la ausencia de un archivo o un permiso insuficiente, entre muchas otras causas. Lo que diferencia a un programa robusto de uno frágil no es la ausencia de errores, sino la capacidad de anticiparlos y manejarlos de manera controlada. En lugar de permitir que un error provoque la detención abrupta e inesperada del programa, Python ofrece un conjunto de herramientas que permiten "atrapar" estas situaciones problemáticas y reaccionar ante ellas de forma adecuada, ya sea registrando el problema, reintentando la operación, o continuando con el resto del programa sin verse afectado.

Esta capacidad resulta particularmente crítica en el desarrollo de herramientas de ciberseguridad, donde es habitual interactuar con sistemas externos —hosts remotos, servicios de red, archivos de configuración, APIs— cuyo comportamiento no siempre es predecible: un host puede no responder, una conexión puede rechazarse, un archivo de wordlist puede no existir, o un servicio puede devolver datos en un formato distinto al esperado. Un script que no contempla estos escenarios tiende a interrumpirse ante el primer imprevisto, mientras que un script bien diseñado puede continuar operando, informar el problema con claridad, o tomar una acción alternativa.

## Excepciones

Una excepción, en Python, es un evento que ocurre durante la ejecución de un programa y que interrumpe el flujo normal de sus instrucciones. Cuando el intérprete se encuentra con una situación que no puede resolver por sí mismo —como dividir un número entre cero, acceder a un índice inexistente de una lista, o intentar convertir una cadena no numérica a un entero— "levanta" o "arroja" una excepción, deteniendo la ejecución secuencial del programa en ese punto, a menos que dicha excepción sea capturada y manejada explícitamente.

Python organiza sus excepciones en una jerarquía de clases incorporadas, cada una representando un tipo específico de error: `ValueError` para valores con un tipo correcto pero un contenido inapropiado, `TypeError` para operaciones aplicadas sobre tipos de datos incompatibles, `KeyError` para el acceso a una clave inexistente en un diccionario, `IndexError` para el acceso a una posición inexistente en una lista, `ConnectionError` y sus subclases (como `ConnectionRefusedError` o `TimeoutError`) para problemas relacionados con conexiones de red, y `FileNotFoundError` para intentos de acceso a archivos inexistentes, entre muchas otras.

## Bloques `try` y `except`

Para manejar excepciones de forma controlada, Python utiliza los bloques `try` y `except`. El bloque `try` contiene el fragmento de código que potencialmente puede generar una excepción, mientras que el bloque `except` define el código que debe ejecutarse en caso de que dicha excepción efectivamente se produzca, evitando así que el programa se detenga de forma abrupta.

```python
import socket

host = "192.168.1.250"
puerto = 22

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((host, puerto))
    print(f"Conexión exitosa con {host}:{puerto}")
except ConnectionRefusedError:
    print(f"El host {host} rechazó la conexión en el puerto {puerto}")
```

Es posible, y en general recomendable, capturar distintos tipos de excepciones por separado, definiendo varios bloques `except` consecutivos, cada uno orientado a un tipo de error específico. Esto permite que el programa reaccione de forma diferenciada según la naturaleza concreta del problema, en lugar de tratar todos los errores de manera idéntica.

```python
import socket

host = "192.168.1.250"
puerto = 22

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((host, puerto))
    print(f"Conexión exitosa con {host}:{puerto}")
except ConnectionRefusedError:
    print(f"El host {host} rechazó la conexión en el puerto {puerto}")
except socket.timeout:
    print(f"El host {host} no respondió a tiempo (timeout)")
except socket.gaierror:
    print(f"No se pudo resolver el nombre de host: {host}")
```

También es posible capturar una excepción sin especificar su tipo concreto, utilizando simplemente `except Exception`, lo que permite atrapar cualquier error que herede de la clase base `Exception`. Si bien esta forma resulta más permisiva y puede ser útil como mecanismo de seguridad general al final de una cadena de bloques `except`, su uso indiscriminado como única forma de manejo de errores se considera una mala práctica, ya que oculta la causa real del problema y dificulta su diagnóstico.

```python
try:
    puerto = int("ochenta")   # esto produce un ValueError
except Exception as error:
    print(f"Ocurrió un error inesperado: {error}")
```

Capturar la excepción mediante la cláusula `as error`, como en el ejemplo anterior, permite acceder al objeto de la excepción generada, lo cual habilita la posibilidad de inspeccionar su mensaje descriptivo o registrarlo en un archivo de log, en lugar de simplemente descartar la información del error ocurrido.

## Otras Palabras Clave de Manejo de Excepciones

### La Cláusula `else`

De forma similar a lo visto previamente en los bucles `for` y `while`, los bloques `try`/`except` también admiten una cláusula `else`. En este contexto, el bloque `else` se ejecuta únicamente si el bloque `try` finalizó su ejecución sin que se produjera ninguna excepción. Esta cláusula resulta útil para separar claramente el código que podría fallar (ubicado dentro del `try`) del código que debe ejecutarse solo en caso de éxito, evitando que este último quede involuntariamente "protegido" dentro del mismo bloque `try`, lo que podría ocultar errores que en realidad provienen de esa segunda sección del código.

```python
import socket

host = "192.168.1.10"
puerto = 22

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((host, puerto))
except ConnectionRefusedError:
    print(f"El host {host} rechazó la conexión en el puerto {puerto}")
else:
    # Este bloque solo se ejecuta si la conexión se estableció sin errores
    print(f"Puerto {puerto} confirmado como abierto en {host}")
    sock.close()
```

### La Cláusula `finally`

La cláusula `finally` define un bloque de código que se ejecuta siempre, independientemente de si se produjo una excepción o no, e incluso si dicha excepción no fue capturada por ningún bloque `except`. Esta característica la convierte en el lugar ideal para realizar tareas de limpieza que deben llevarse a cabo sin excepción, como cerrar una conexión de red abierta, liberar un archivo, o restaurar el estado de un recurso compartido, garantizando que estas operaciones se ejecuten tanto si la operación principal tuvo éxito como si falló.

```python
import socket

host = "192.168.1.10"
puerto = 22
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)

try:
    sock.connect((host, puerto))
    print(f"Conexión exitosa con {host}:{puerto}")
except ConnectionRefusedError:
    print(f"El host {host} rechazó la conexión en el puerto {puerto}")
finally:
    # Este bloque se ejecuta sí o sí, haya habido error o no
    sock.close()
    print("Conexión cerrada (recurso liberado)")
```

Es posible, y habitual, combinar `try`, múltiples bloques `except`, `else` y `finally` dentro de una misma estructura, respetando siempre el orden: primero `try`, luego los distintos `except`, después `else`, y finalmente `finally`.

## Levantar Excepciones con `raise`

Además de capturar excepciones generadas automáticamente por el intérprete, Python permite levantar una excepción de forma intencional mediante la palabra clave `raise`. Esto resulta útil cuando se necesita interrumpir la ejecución de una función o de un bloque de código al detectar una condición inválida que el propio programador define como un error, aun cuando dicha condición no provocaría, por sí sola, un error nativo del intérprete.

```python
def validar_puerto(puerto):
    """Valida que el número de puerto se encuentre dentro del rango permitido."""
    if not (1 <= puerto <= 65535):
        raise ValueError(f"Puerto inválido: {puerto}. Debe estar entre 1 y 65535")
    return puerto

try:
    validar_puerto(70000)
except ValueError as error:
    print(f"Error de validación: {error}")
```

El uso de `raise` también permite definir y levantar excepciones personalizadas, creadas a partir de una clase propia que hereda de `Exception`, lo cual resulta especialmente valioso al desarrollar herramientas más grandes, como un escáner de red o un framework de explotación, donde resulta conveniente distinguir los errores específicos de la propia herramienta de los errores genéricos del lenguaje.

```python
class HostInalcanzableError(Exception):
    """Excepción personalizada para indicar que un host no responde al escaneo."""
    pass

def verificar_host(host, responde):
    if not responde:
        raise HostInalcanzableError(f"El host {host} no respondió al escaneo")
    return True

try:
    verificar_host("192.168.1.250", responde=False)
except HostInalcanzableError as error:
    print(f"Fallo en la verificación: {error}")
```

El manejo adecuado de excepciones, combinando `try`, `except`, `else`, `finally` y `raise` según corresponda, es lo que en definitiva permite que un script de ciberseguridad pueda enfrentarse a la naturaleza impredecible de los sistemas y redes con los que interactúa, continuando su ejecución de forma resiliente, informando los problemas encontrados de manera clara, y evitando que un único host caído o una única conexión rechazada interrumpa por completo el resultado de todo un proceso de reconocimiento o de prueba.
