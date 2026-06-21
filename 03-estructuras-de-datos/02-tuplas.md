# Tuplas: Estructura, Operaciones y Buenas Prácticas

## Introducción

Las tuplas son colecciones ordenadas de elementos que, a diferencia de las listas, no pueden modificarse una vez creadas. Esta inmutabilidad no es una limitación accidental del lenguaje, sino una decisión de diseño deliberada: las tuplas existen precisamente para representar datos que deben permanecer constantes a lo largo del ciclo de vida de un programa, comunicando esa intención de forma explícita tanto al intérprete como a cualquier persona que lea el código. En un script de ciberseguridad, este tipo de garantía resulta valiosa para representar, por ejemplo, las coordenadas fijas de un endpoint (host, puerto), un par usuario-contraseña que no debe alterarse accidentalmente durante su procesamiento, o el resultado consolidado de una operación que ya fue completada y no debería seguir modificándose.

## Características de las Tuplas

### Inmutabilidad

Una vez creada una tupla, no es posible cambiar, añadir o eliminar ninguno de sus elementos. Cualquier intento de modificar una tupla directamente produce un error de tipo `TypeError`. Esta inmutabilidad garantiza la integridad de los datos que se desea mantener constantes, evitando que una sección del programa modifique, intencional o accidentalmente, datos que otra sección del mismo programa asume como fijos.

```python
endpoint = ("192.168.1.10", 443)

# endpoint[1] = 8443   # TypeError: 'tuple' object does not support item assignment
```

Es importante matizar este concepto con un detalle avanzado: la inmutabilidad de una tupla es **superficial**. Lo que resulta inmutable es la propia tupla en sí, es decir, la asociación entre sus posiciones y los objetos que contiene; pero si uno de esos objetos es, a su vez, una estructura mutable (como una lista), el contenido interno de dicho objeto sí puede modificarse, aunque la tupla que lo contiene continúe siendo, en apariencia, inalterable.

```python
registro_host = ("192.168.1.10", [22, 80, 443])   # una tupla que contiene una lista mutable

registro_host[1].append(445)   # esto SÍ es válido: se modifica la lista interna, no la tupla
print(registro_host)   # ('192.168.1.10', [22, 80, 443, 445])

# registro_host[1] = []   # esto SÍ fallaría: no se puede reasignar la posición de la tupla
```

### Indexación y _Slicing_

Al igual que ocurre con las listas, los elementos de una tupla pueden accederse mediante índices, comenzando desde `0` para el primer elemento y admitiendo índices negativos para contar desde el final. Asimismo, las tuplas admiten _slicing_, devolviendo como resultado una nueva tupla con la subsecuencia correspondiente, en lugar de una lista.

```python
coordenada_red = ("192.168.1.0", "255.255.255.0", "192.168.1.1", "8.8.8.8")

red = coordenada_red[0]            # "192.168.1.0"
dns_secundario = coordenada_red[-1]  # "8.8.8.8"
rango_principal = coordenada_red[0:2]   # ("192.168.1.0", "255.255.255.0")  <- sigue siendo una tupla
```

### Heterogeneidad y Tuplas Anidadas

Las tuplas, al igual que las listas, pueden contener elementos de distintos tipos de datos dentro de una misma colección, incluyendo otras tuplas anidadas en su interior. Esta capacidad las vuelve adecuadas para representar registros estructurados de longitud fija, donde cada posición tiene un significado semántico particular y conocido de antemano, como ocurre con una fila de resultados que combina una dirección IP, un número de puerto y un valor booleano de estado.

```python
# Una tupla puede combinar tipos heterogéneos, incluyendo otra tupla anidada
hallazgo = ("192.168.1.10", 445, "SMB", True, ("CVE-2020-1472", 10.0))

cve_asociado = hallazgo[4][0]   # "CVE-2020-1472"
```

## Tuplas frente a Listas: ¿Cuándo Usar Cada Una?

Antes de profundizar en las operaciones disponibles, conviene detenerse en una pregunta de diseño recurrente: si las tuplas son tan similares a las listas pero más restrictivas, ¿qué ventaja concreta justifica su uso? La respuesta involucra al menos tres factores.

En primer lugar, la **intención semántica**: declarar una colección como tupla comunica explícitamente que se trata de un conjunto de datos fijo y cerrado, mientras que una lista comunica una colección potencialmente dinámica. Esta distinción ayuda a que el código se autodocumente y reduce la posibilidad de errores derivados de modificaciones no previstas.

En segundo lugar, el **rendimiento**: las tuplas, al ser inmutables, permiten al intérprete de Python aplicar ciertas optimizaciones internas que no son posibles con las listas, resultando en una creación e iteración ligeramente más eficientes, además de ocupar, en general, menos memoria que una lista con el mismo contenido.

En tercer lugar, y quizás el más relevante en términos prácticos, la **hashabilidad**: por ser inmutables, las tuplas (siempre que todos sus elementos también lo sean) pueden utilizarse como claves de un diccionario o como elementos de un `set`, algo que las listas, al ser mutables, tienen explícitamente prohibido. Esta propiedad resulta sumamente útil en ciberseguridad para indexar resultados por una combinación de valores, como un par (host, puerto), dentro de una estructura de búsqueda rápida.

```python
# Las tuplas SÍ pueden usarse como clave de un diccionario; las listas, no
estado_servicios = {
    ("192.168.1.10", 22): "abierto",
    ("192.168.1.10", 443): "abierto",
    ("192.168.1.11", 22): "filtrado",
}

print(estado_servicios[("192.168.1.10", 443)])   # "abierto"

# estado_servicios[["192.168.1.10", 22]] = "abierto"   # TypeError: unhashable type: 'list'
```

## Operaciones con Tuplas

Aunque una tupla no puede modificarse una vez creada, esto no significa que las operaciones disponibles sobre ella sean limitadas: existen varias formas de combinar, recorrer, consultar y transformar tuplas, generando siempre, cuando corresponde, una nueva tupla en lugar de alterar la existente.

### Empaquetado y Desempaquetado (_Packing_ y _Unpacking_)

El empaquetado de tuplas consiste en agrupar varios valores en una única tupla simplemente separándolos por comas, incluso sin necesidad de utilizar paréntesis explícitos, ya que es la coma, y no el paréntesis, lo que define a una tupla en Python. El desempaquetado es la operación inversa: permite asignar, en una única línea, cada uno de los elementos de una tupla a una variable distinta, siempre que la cantidad de variables coincida con la cantidad de elementos de la tupla.

```python
# Empaquetado: los paréntesis son opcionales, lo que define la tupla es la coma
registro = "192.168.1.10", 443, "https"   # esto ya es una tupla

# Desempaquetado: asignación simultánea de cada elemento a una variable
host, puerto, protocolo = registro
print(host, puerto, protocolo)   # 192.168.1.10 443 https
```

El desempaquetado también admite una sintaxis extendida mediante el operador `*`, que permite capturar en una lista todos los elementos "sobrantes" que no fueron asignados explícitamente a otra variable, lo cual resulta útil cuando se conoce la cantidad de elementos en los extremos de la tupla, pero no necesariamente la cantidad total.

```python
resultado_escaneo = ("192.168.1.10", 22, 80, 443, 445, 3389)

host, *puertos_abiertos = resultado_escaneo
print(host)               # 192.168.1.10
print(puertos_abiertos)   # [22, 80, 443, 445, 3389]   <- nótese que esto es una LISTA, no una tupla

primero, *intermedios, ultimo = resultado_escaneo
print(primero, intermedios, ultimo)   # 192.168.1.10 [22, 80, 443, 445] 3389
```

Una aplicación frecuente del empaquetado y desempaquetado consiste en intercambiar los valores de dos variables sin necesidad de una variable temporal auxiliar, aprovechando que Python empaqueta primero el lado derecho de la asignación en una tupla y luego la desempaqueta sobre el lado izquierdo:

```python
puerto_origen, puerto_destino = 22, 443
puerto_origen, puerto_destino = puerto_destino, puerto_origen   # intercambio directo
print(puerto_origen, puerto_destino)   # 443 22
```

### Concatenación y Repetición

De forma análoga a lo visto con las listas, el operador `+` permite concatenar dos tuplas, generando una nueva tupla que contiene los elementos de ambas en el orden en que fueron combinadas, mientras que el operador `*` permite repetir el contenido de una tupla un número determinado de veces. En ambos casos, dado que las tuplas son inmutables, el resultado es siempre una tupla **nueva**, sin que las tuplas originales se vean alteradas.

```python
puertos_tcp_comunes = (21, 22, 23)
puertos_web = (80, 443)

todos_los_puertos = puertos_tcp_comunes + puertos_web
print(todos_los_puertos)   # (21, 22, 23, 80, 443)

marcador_repetido = ("---",) * 3   # nótese la coma: es necesaria para que sea una tupla de un elemento
print(marcador_repetido)   # ('---', '---', '---')
```

### Métodos de Búsqueda: `index()` y `count()`

Dado que las tuplas no admiten operaciones que modifiquen su contenido, su conjunto de métodos disponibles es deliberadamente reducido, limitándose esencialmente a dos: `index()`, que devuelve la posición de la primera ocurrencia de un valor dado dentro de la tupla (lanzando un `ValueError` si dicho valor no se encuentra), y `count()`, que devuelve la cantidad de veces que un valor determinado aparece en la tupla.

```python
puertos_detectados = (22, 80, 443, 80, 8080)

posicion = puertos_detectados.index(443)   # 2
repeticiones = puertos_detectados.count(80)   # 2 (el puerto 80 aparece dos veces)

print(posicion, repeticiones)
```

## Uso de Tuplas en Python

### Funciones que Devuelven Múltiples Valores

Una de las aplicaciones más habituales de las tuplas en código real es permitir que una función devuelva múltiples valores de forma simultánea. En realidad, Python no admite que una función devuelva literalmente "varios valores": lo que ocurre internamente es que dichos valores se empaquetan de forma automática en una única tupla, que luego puede desempaquetarse directamente en el punto donde se invoca la función.

```python
def analizar_host(ip):
    """Devuelve, de forma simultánea, el estado y el tiempo de respuesta simulado de un host."""
    activo = True
    tiempo_respuesta = 0.045
    return activo, tiempo_respuesta   # esto se empaqueta automáticamente en una tupla

esta_activo, tiempo = analizar_host("192.168.1.10")
print(f"Activo: {esta_activo} - Tiempo: {tiempo}s")
```

### Asignaciones Múltiples

El desempaquetado de tuplas también permite inicializar varias variables relacionadas entre sí en una única línea, una práctica habitual al definir constantes de configuración relacionadas, como el rango de red y la puerta de enlace de un entorno de laboratorio.

```python
red_objetivo, mascara, gateway = "192.168.1.0/24", "255.255.255.0", "192.168.1.1"
```

### Estructuras de Datos Fijas

Las tuplas resultan especialmente adecuadas para representar colecciones de valores que, por su propia naturaleza, no deberían cambiar durante la ejecución del programa: los nombres de los días de la semana, las coordenadas de un punto en un plano, los códigos de estado HTTP relevantes para una herramienta determinada, o el conjunto de protocolos que una herramienta de escaneo está diseñada para reconocer.

```python
PROTOCOLOS_SOPORTADOS = ("tcp", "udp", "icmp")
CODIGOS_HTTP_INTERESANTES = (200, 301, 302, 401, 403, 500)
```

El uso de tuplas para este tipo de constantes, frecuentemente combinado con la convención de escribir su nombre en mayúsculas (siguiendo PEP 8), comunica de forma inmediata que se trata de un conjunto de valores que no debe modificarse a lo largo de la ejecución del programa, reforzando con la propia estructura de datos lo que la convención de nomenclatura ya sugiere.

### Tuplas como Claves de Diccionario en Estructuras de Búsqueda

Tal como se mencionó al comparar tuplas con listas, una aplicación particularmente potente de las tuplas en ciberseguridad consiste en utilizarlas como clave de un diccionario para indexar resultados según una combinación de valores, en lugar de un único valor simple. Esto resulta natural al trabajar con resultados de escaneo, donde un mismo host puede tener múltiples puertos, y la combinación (host, puerto) identifica de forma única a cada servicio detectado.

```python
inventario_servicios = {}

inventario_servicios[("192.168.1.10", 22)] = {"servicio": "ssh", "version": "OpenSSH 8.2"}
inventario_servicios[("192.168.1.10", 443)] = {"servicio": "https", "version": "nginx 1.18"}

clave_consultada = ("192.168.1.10", 443)
if clave_consultada in inventario_servicios:
    print(inventario_servicios[clave_consultada])
```

### _Named Tuples_: Tuplas con Campos Identificados por Nombre

Un aspecto avanzado que vale la pena conocer es que la biblioteca estándar de Python ofrece, dentro del módulo `collections`, una utilidad llamada `namedtuple`, que permite crear tuplas cuyos elementos pueden accederse tanto por posición como por nombre, combinando la inmutabilidad y eficiencia de las tuplas con la legibilidad de acceder a sus campos mediante un atributo con nombre, en lugar de un índice numérico difícil de recordar.

```python
from collections import namedtuple

Hallazgo = namedtuple("Hallazgo", ["host", "puerto", "servicio", "cvss"])

hallazgo_1 = Hallazgo(host="192.168.1.10", puerto=445, servicio="smb", cvss=10.0)

# Acceso por nombre (mucho más legible que hallazgo_1[0], hallazgo_1[1], etc.)
print(f"{hallazgo_1.host}:{hallazgo_1.puerto} ({hallazgo_1.servicio}) - CVSS {hallazgo_1.cvss}")

# Sigue siendo, además, una tupla normal: admite indexación y desempaquetado
print(hallazgo_1[0])                      # "192.168.1.10"
host, puerto, servicio, cvss = hallazgo_1  # desempaquetado estándar
```

El uso de `namedtuple` resulta especialmente recomendable cuando una tupla representa un registro estructurado con varios campos cuyo significado no resulta evidente a partir de su posición numérica, como ocurre con un hallazgo de auditoría compuesto por varios atributos: en estos casos, los nombres explícitos de los campos mejoran sustancialmente la legibilidad del código frente al uso de índices numéricos sueltos.

## Buenas Prácticas en el Uso de Tuplas

A la hora de decidir entre utilizar una tupla o una lista, conviene aplicar un criterio simple basado en la naturaleza de los datos: si la colección representa un conjunto de valores relacionados y fijo, cuya cantidad y significado de cada posición se conocen de antemano y no deberían cambiar (como una coordenada, un par host-puerto, o una fila de resultados ya calculada), una tupla es la elección más apropiada. Si, en cambio, la colección representa una secuencia homogénea de elementos que crecerá, se modificará o se reordenará a lo largo de la ejecución del programa (como una lista de hosts descubiertos progresivamente durante un escaneo), una lista resulta más adecuada.

También es recomendable aprovechar el desempaquetado de tuplas siempre que sea posible, en lugar de acceder a los elementos mediante índices numéricos sueltos, ya que la primera forma resulta considerablemente más legible y menos propensa a errores al modificar el código en el futuro. De forma relacionada, cuando una tupla representa un registro con varios campos cuyo significado podría no resultar evidente a simple vista, conviene evaluar el uso de `namedtuple` en lugar de una tupla simple, especialmente en estructuras de datos que se reutilizarán en múltiples puntos de un proyecto de mayor tamaño, como ocurre en una herramienta propia de reconocimiento o en un parser de resultados de escaneo.

Finalmente, conviene recordar que la inmutabilidad de una tupla es superficial: si se almacena una lista u otro objeto mutable dentro de una tupla, dicho objeto interno seguirá siendo modificable. Quien diseña una estructura de datos basada en tuplas con el objetivo de garantizar inmutabilidad debe asegurarse, por lo tanto, de que todos los elementos contenidos sean, a su vez, inmutables (números, cadenas, booleanos u otras tuplas), si la integridad completa de los datos es un requisito real del programa.