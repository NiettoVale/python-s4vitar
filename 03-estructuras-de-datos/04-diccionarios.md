# Diccionarios: Estructura, Operaciones y Buenas Prácticas

## Introducción

Los diccionarios son colecciones de pares clave-valor que permiten asociar un dato (el valor) a un identificador único (la clave). A diferencia de las secuencias vistas hasta ahora —listas y tuplas—, que se indexan mediante un rango numérico fijo comenzando en `0`, los diccionarios se indexan mediante claves, que pueden ser de cualquier tipo inmutable y _hashable_, como cadenas, números o tuplas. Esta diferencia conceptual es lo que convierte a los diccionarios en la estructura de elección cuando los datos a representar tienen una relación natural de identificador-valor, en lugar de una simple secuencia posicional, algo extremadamente frecuente en ciberseguridad: el resultado de un escaneo asociado a una dirección IP, los metadatos de un CVE asociados a su identificador, o la configuración de una herramienta asociada al nombre de cada parámetro.

## Características de los Diccionarios

### Desordenados (con un Matiz Histórico Importante)

Conceptualmente, los diccionarios se consideran colecciones desordenadas, en el sentido de que no se accede a sus elementos mediante una posición numérica, sino exclusivamente a través de su clave. Sin embargo, vale la pena precisar un detalle relevante de la implementación actual del lenguaje: desde Python 3.7, los diccionarios garantizan, como parte formal de la especificación del lenguaje, que preservan el **orden de inserción** de sus elementos al recorrerlos. Esto significa que, en la práctica, si se itera sobre un diccionario moderno, sus pares aparecerán en el mismo orden en que fueron agregados. Pese a esta garantía, sigue sin ser correcto pensar en un diccionario como una estructura indexada por posición: no existe la noción de "el tercer elemento del diccionario" de la misma forma en que existe "el tercer elemento de una lista", y la garantía de orden de inserción no debe confundirse con la posibilidad de acceder por índice numérico.

```python
resultado_escaneo = {}
resultado_escaneo["host"] = "192.168.1.10"
resultado_escaneo["puerto"] = 443
resultado_escaneo["servicio"] = "https"

# Desde Python 3.7+, el orden de inserción se preserva al iterar
for clave, valor in resultado_escaneo.items():
    print(f"{clave}: {valor}")   # se imprime en el orden en que se agregaron: host, puerto, servicio
```

### Dinámicos

Los diccionarios son estructuras mutables: es posible agregar nuevos pares clave-valor, modificar el valor asociado a una clave existente, y eliminar pares por completo, todo después de la creación del diccionario. Esta flexibilidad los hace especialmente adecuados para construir estructuras de datos que se completan progresivamente a lo largo de la ejecución de un script, como un reporte que se va enriqueciendo a medida que avanza un proceso de reconocimiento.

### Claves Únicas

Cada clave dentro de un diccionario es única: si se intenta asignar un valor a una clave que ya existe, el nuevo valor sobrescribe al anterior, en lugar de generar un error o crear una entrada duplicada. Esta propiedad previene de forma natural las duplicaciones accidentales, pero también implica que se debe prestar atención al reutilizar una misma clave sin darse cuenta, ya que esto provoca la pérdida silenciosa del valor previamente almacenado.

```python
puertos_por_host = {}
puertos_por_host["192.168.1.10"] = [22, 80]
puertos_por_host["192.168.1.10"] = [443]   # esto SOBRESCRIBE el valor anterior, no lo combina

print(puertos_por_host)   # {'192.168.1.10': [443]}   <- se perdió el [22, 80] original
```

### Restricción de las Claves: Deben Ser _Hashables_

Al igual que ocurría con los elementos de un conjunto, las claves de un diccionario deben ser de un tipo inmutable y _hashable_: cadenas, números, booleanos o tuplas (siempre que estas, a su vez, solo contengan elementos inmutables). No es posible utilizar una lista ni otro diccionario como clave, precisamente porque ambos son mutables. Los **valores**, en cambio, no tienen esta restricción y pueden ser de cualquier tipo de dato, incluyendo listas, otros diccionarios, o incluso funciones.

```python
inventario = {
    ("192.168.1.10", 443): "https",   # tupla como clave: válido, es inmutable
}

# inventario[["192.168.1.10", 443]] = "https"   # TypeError: unhashable type: 'list'
```

## Operaciones con Diccionarios

### Agregar y Modificar Elementos

Un nuevo par clave-valor se agrega simplemente asignando un valor a una clave que aún no existe en el diccionario, utilizando la misma sintaxis de corchetes que se emplea para modificar el valor de una clave ya existente; Python no distingue sintácticamente entre ambas operaciones, sino que decide automáticamente si crea una entrada nueva o sobrescribe una existente según si la clave ya estaba presente.

```python
host_info = {"ip": "192.168.1.10", "estado": "activo"}

host_info["puerto_principal"] = 443   # agrega una clave nueva
host_info["estado"] = "comprometido"   # modifica el valor de una clave existente

print(host_info)
```

### Acceso a Valores: Corchetes frente a `get()`

Existen dos formas principales de obtener el valor asociado a una clave. Acceder mediante corchetes, como en `diccionario[clave]`, produce un error de tipo `KeyError` si la clave no existe, lo que resulta apropiado cuando se tiene la certeza de que la clave debería estar presente y su ausencia representa, en sí misma, una condición anómala. El método `get()`, en cambio, devuelve `None` (o un valor por defecto que puede especificarse explícitamente como segundo argumento) si la clave no se encuentra, en lugar de lanzar una excepción, lo cual resulta más apropiado cuando la ausencia de la clave es un escenario esperado y normal dentro de la lógica del programa.

```python
configuracion = {"timeout": 5, "reintentos": 3}

# Acceso directo: lanza KeyError si la clave no existe
valor_timeout = configuracion["timeout"]

# get(): devuelve None (o un valor por defecto) si la clave no existe, sin error
valor_proxy = configuracion.get("proxy")                  # None, ya que "proxy" no está definida
valor_proxy_con_default = configuracion.get("proxy", "sin definir")   # "sin definir"

print(valor_timeout, valor_proxy, valor_proxy_con_default)
```

### Eliminar Elementos: `del`, `pop()`, `popitem()` y `clear()`

La sentencia `del diccionario[clave]` elimina por completo el par correspondiente a esa clave, lanzando un `KeyError` si la clave no existe. El método `pop(clave)` realiza una eliminación equivalente, pero además **devuelve el valor** que estaba asociado a la clave eliminada, lo cual resulta útil cuando se necesita tanto eliminar como reutilizar ese valor; `pop()` también admite un segundo argumento opcional con un valor por defecto a devolver si la clave no existe, evitando así el `KeyError`. El método `popitem()`, por su parte, elimina y devuelve el último par clave-valor insertado en el diccionario, siguiendo el orden de inserción mencionado anteriormente. Finalmente, `clear()` elimina la totalidad de los pares, dejando el diccionario vacío.

```python
sesiones_activas = {"sess_001": "192.168.1.10", "sess_002": "192.168.1.11"}

del sesiones_activas["sess_001"]
print(sesiones_activas)   # {'sess_002': '192.168.1.11'}

ip_cerrada = sesiones_activas.pop("sess_002")
print(ip_cerrada)   # "192.168.1.11"

ultima_entrada = {"a": 1, "b": 2, "c": 3}
clave, valor = ultima_entrada.popitem()
print(clave, valor)   # "c", 3   <- el último par insertado
```

### Métodos de Vista: `keys()`, `values()` e `items()`

Python ofrece tres métodos que permiten acceder, respectivamente, a las claves, a los valores, o a ambos en forma de pares (tuplas), dentro de un diccionario. Estos métodos no devuelven listas, sino objetos de tipo _vista_ (`dict_keys`, `dict_values` y `dict_items`), los cuales tienen una característica avanzada particular: son **dinámicos**, es decir, reflejan automáticamente cualquier cambio posterior realizado sobre el diccionario original, sin necesidad de volver a invocar el método.

```python
resultado = {"host": "192.168.1.10", "puerto": 443}

vista_claves = resultado.keys()
print(list(vista_claves))   # ['host', 'puerto']

resultado["servicio"] = "https"   # se modifica el diccionario DESPUÉS de obtener la vista

print(list(vista_claves))   # ['host', 'puerto', 'servicio']   <- la vista reflejó el cambio automáticamente
```

El método `items()` resulta particularmente útil al combinarse con un bucle `for`, ya que permite desempaquetar directamente cada clave y su valor correspondiente en una sola línea, sin necesidad de acceder al valor por separado mediante `diccionario[clave]` dentro del cuerpo del bucle.

```python
puertos_por_servicio = {"ssh": 22, "https": 443, "smb": 445}

for servicio, puerto in puertos_por_servicio.items():
    print(f"El servicio {servicio} utiliza el puerto {puerto}")
```

### `setdefault()`: Obtener o Inicializar en una Sola Operación

Un método avanzado, pero muy útil en la práctica, es `setdefault(clave, valor_por_defecto)`: si la clave ya existe en el diccionario, devuelve su valor actual sin modificarlo; si la clave no existe, la crea con el valor por defecto indicado y devuelve ese mismo valor. Este método resulta especialmente conveniente para agrupar datos progresivamente sin tener que verificar manualmente, en cada iteración, si la clave ya fue inicializada.

```python
hallazgos_por_host = {}

eventos = [
    ("192.168.1.10", "puerto 445 abierto"),
    ("192.168.1.10", "SMBv1 habilitado"),
    ("192.168.1.11", "puerto 22 abierto"),
]

for host, hallazgo in eventos:
    # Si el host aún no tiene una lista asociada, setdefault() la crea como []
    hallazgos_por_host.setdefault(host, []).append(hallazgo)

print(hallazgos_por_host)
# {'192.168.1.10': ['puerto 445 abierto', 'SMBv1 habilitado'], '192.168.1.11': ['puerto 22 abierto']}
```

Este mismo patrón de agrupación progresiva puede resolverse de forma aún más directa utilizando `defaultdict`, una estructura disponible en el módulo `collections` de la biblioteca estándar, que permite definir un valor por defecto automático para cualquier clave nueva, eliminando la necesidad de invocar `setdefault()` explícitamente en cada iteración.

```python
from collections import defaultdict

hallazgos_por_host = defaultdict(list)   # toda clave nueva arranca automáticamente con una lista vacía

for host, hallazgo in eventos:
    hallazgos_por_host[host].append(hallazgo)   # ya no hace falta setdefault()

print(dict(hallazgos_por_host))
```

### Combinar Diccionarios: `update()`, el Operador `|` y el Desempaquetado `**`

Para fusionar el contenido de dos diccionarios, Python ofrece varias alternativas. El método `update()` incorpora al diccionario sobre el que se invoca todos los pares de otro diccionario (o de cualquier iterable de pares), sobrescribiendo los valores de las claves que coincidan entre ambos, y modificando el diccionario original directamente. Desde Python 3.9, el operador `|` permite fusionar dos diccionarios devolviendo un **nuevo** diccionario, sin modificar ninguno de los dos originales, de forma análoga a como `|` se utiliza con conjuntos. También es posible combinar diccionarios mediante el operador de desempaquetado `**` dentro de la definición de un nuevo diccionario literal.

```python
configuracion_base = {"timeout": 5, "reintentos": 3}
configuracion_usuario = {"reintentos": 10, "verbose": True}

# update(): modifica configuracion_base directamente
configuracion_base.update(configuracion_usuario)
print(configuracion_base)   # {'timeout': 5, 'reintentos': 10, 'verbose': True}

# Operador |: genera un nuevo diccionario, sin modificar los originales (Python 3.9+)
base = {"timeout": 5, "reintentos": 3}
usuario = {"reintentos": 10, "verbose": True}
configuracion_final = base | usuario
print(configuracion_final)

# Desempaquetado **: equivalente, también genera un diccionario nuevo
configuracion_final_v2 = {**base, **usuario}
print(configuracion_final_v2)
```

En todos los casos, cuando una misma clave está presente en ambos diccionarios, el valor del segundo diccionario (el que se pasa como argumento, o el que aparece más a la derecha) prevalece sobre el del primero.

### Comprensión de Diccionarios

De forma análoga a la comprensión de listas y de conjuntos, Python admite la comprensión de diccionarios, utilizando la sintaxis `{clave: valor for elemento in iterable}`, opcionalmente con una cláusula `if` para filtrar. Esta construcción resulta extremadamente útil para transformar una secuencia existente en un diccionario, o para transformar un diccionario en otro con sus claves, valores, o ambos modificados.

```python
puertos = [21, 22, 80, 443, 445]

# Construir un diccionario que asocie cada puerto con un booleano de "es crítico"
puertos_criticos_conocidos = {21, 23, 445, 3389}
estado_criticidad = {p: (p in puertos_criticos_conocidos) for p in puertos}
print(estado_criticidad)   # {21: True, 22: False, 80: False, 443: False, 445: True}

# Invertir un diccionario existente: de {clave: valor} a {valor: clave}
puertos_por_servicio = {"ssh": 22, "https": 443, "smb": 445}
servicio_por_puerto = {puerto: servicio for servicio, puerto in puertos_por_servicio.items()}
print(servicio_por_puerto)   # {22: 'ssh', 443: 'https', 445: 'smb'}
```

## Uso de Diccionarios en Python

### Almacenamiento de Datos Estructurados

Los diccionarios son ideales para almacenar y organizar datos relacionados entre sí de forma lógica, funcionando en la práctica como una base de datos en memoria de estructura simple. Esta capacidad se vuelve aún más evidente al observar que el formato **JSON**, ampliamente utilizado para el intercambio de datos entre APIs, servicios web y herramientas de ciberseguridad, se traduce de forma prácticamente directa a diccionarios de Python al ser parseado, lo que convierte al manejo fluido de diccionarios en una habilidad indispensable para interactuar con la salida de prácticamente cualquier herramienta o API moderna.

```python
import json

respuesta_api_simulada = '{"cve_id": "CVE-2024-1234", "severidad": "alta", "afectados": ["192.168.1.10"]}'
datos = json.loads(respuesta_api_simulada)   # se convierte directamente en un diccionario de Python

print(datos["cve_id"], datos["severidad"], datos["afectados"])
```

### Búsqueda Eficiente

Al igual que los conjuntos, los diccionarios están implementados internamente mediante una tabla hash, lo que les otorga un rendimiento de búsqueda promedio constante, `O(1)`, al recuperar un valor a partir de su clave, independientemente del tamaño del diccionario. Esta característica los vuelve muy superiores a una lista de tuplas `(clave, valor)` cuando se necesita realizar búsquedas frecuentes por clave, ya que en una lista esa búsqueda requeriría, en el peor caso, recorrerla por completo.

### Flexibilidad: Diccionarios Anidados

Los valores de un diccionario pueden ser, a su vez, otros diccionarios, listas, o cualquier otro tipo de dato, lo que permite construir estructuras de datos jerárquicas capaces de representar información compleja, como el resultado completo de un escaneo de red que agrupa, para cada host, sus puertos abiertos junto con los metadatos de cada servicio detectado.

```python
inventario_red = {
    "192.168.1.10": {
        "estado": "activo",
        "servicios": {
            22: {"nombre": "ssh", "version": "OpenSSH 8.2"},
            443: {"nombre": "https", "version": "nginx 1.18"},
        },
    },
    "192.168.1.11": {
        "estado": "inactivo",
        "servicios": {},
    },
}

# Acceso a un dato anidado, encadenando claves
version_ssh = inventario_red["192.168.1.10"]["servicios"][22]["version"]
print(version_ssh)   # "OpenSSH 8.2"
```

Al trabajar con diccionarios profundamente anidados como este, conviene combinar el acceso encadenado con `get()` en cada nivel cuando no se tiene certeza de que todas las claves intermedias existan, evitando así que un `KeyError` en un nivel intermedio interrumpa abruptamente la ejecución del script al procesar, por ejemplo, una respuesta de API con una estructura ligeramente distinta a la esperada.

## Buenas Prácticas en el Uso de Diccionarios

A la hora de acceder a un valor por su clave, conviene reflexionar sobre si la ausencia de dicha clave representa, en el contexto del programa, un error genuino que debería detener la ejecución (en cuyo caso el acceso directo con corchetes, dejando que el `KeyError` se propague o capturándolo explícitamente, es la opción correcta) o si, por el contrario, se trata de un escenario esperado dentro del flujo normal del programa (en cuyo caso `get()`, con un valor por defecto razonable, resulta más apropiado y produce un código más limpio que rodear cada acceso con un bloque `try`/`except`).

También resulta recomendable aprovechar `setdefault()` o `defaultdict` al construir estructuras de agrupación progresiva, en lugar de verificar manualmente, en cada iteración, si una clave ya existe antes de inicializarla, ya que esta verificación manual añade ruido visual innecesario a una operación conceptualmente simple.

En cuanto al rendimiento, conviene recordar que los diccionarios ofrecen búsquedas por clave extremadamente rápidas, por lo que, frente a la necesidad de buscar repetidamente datos asociados a un identificador conocido —como recuperar la información de un host a partir de su dirección IP—, un diccionario casi siempre será preferible a una lista de tuplas o de diccionarios que deba recorrerse manualmente en cada búsqueda.

Finalmente, al trabajar con diccionarios anidados que representan datos provenientes de fuentes externas, como una respuesta de API o un archivo de configuración, conviene validar la presencia de las claves esperadas de forma defensiva, ya sea mediante `get()` encadenado con valores por defecto, o mediante un manejo explícito de excepciones, en lugar de asumir que la estructura del dato externo siempre coincidirá exactamente con lo esperado, una suposición que en la práctica de la ciberseguridad —donde frecuentemente se procesan respuestas de sistemas heterogéneos y no siempre bien documentados— rara vez se sostiene de forma confiable.
