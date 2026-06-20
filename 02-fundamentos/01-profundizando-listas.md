# Profundización en Listas: Estructura, Operaciones y Buenas Prácticas

## Características de las Listas

Las listas constituyen una de las estructuras de datos más versátiles del lenguaje, y comprender en profundidad sus características es fundamental para utilizarlas de forma eficiente en cualquier script, especialmente en herramientas de ciberseguridad donde con frecuencia se manipulan conjuntos de datos heterogéneos y de tamaño variable, como resultados de escaneos, listas de credenciales o registros de eventos.

### Almacenamiento de Datos Heterogéneos

Una lista puede contener elementos de distintos tipos de datos simultáneamente: enteros, cadenas, flotantes, booleanos, e incluso otras estructuras de datos como diccionarios, tuplas u otras listas, todo dentro de una misma colección. Esta característica diferencia a Python de lenguajes con tipado estático, donde un arreglo suele estar restringido a contener elementos de un único tipo.

```python
# Una lista puede combinar libremente distintos tipos de datos
resultado_host = ["192.168.1.10", 443, True, 0.215, {"servicio": "https"}]
```

Si bien esta flexibilidad resulta cómoda, en la práctica suele ser recomendable mantener cierta consistencia de tipos dentro de una misma lista cuando esta representa una colección conceptualmente homogénea (por ejemplo, una lista de puertos o una lista de hosts), reservando la heterogeneidad para estructuras que deliberadamente agrupan datos de naturaleza distinta, como una fila de resultados.

### Indexación y _Slicing_

Las listas son estructuras indexadas, lo que significa que cada uno de sus elementos ocupa una posición numérica concreta, comenzando desde el índice `0` para el primer elemento. Python permite además el uso de índices negativos, que cuentan las posiciones desde el final de la lista hacia el principio, donde `-1` corresponde siempre al último elemento.

```python
puertos = [21, 22, 23, 80, 443, 445, 3389]

primero = puertos[0]     # 21
ultimo = puertos[-1]     # 3389
penultimo = puertos[-2]  # 445
```

El _slicing_, o corte, permite extraer una sublista a partir de un rango de índices, utilizando la sintaxis `lista[inicio:fin:paso]`, donde `inicio` es el índice del primer elemento incluido (por defecto `0`), `fin` es el índice del primer elemento **excluido** (por defecto, el final de la lista), y `paso` indica cada cuántos elementos se debe avanzar (por defecto `1`).

```python
puertos = [21, 22, 23, 80, 443, 445, 3389]

primeros_tres = puertos[0:3]      # [21, 22, 23]
desde_el_cuarto = puertos[3:]     # [80, 443, 445, 3389]
alternados = puertos[::2]         # [21, 23, 443, 3389] (un elemento sí, uno no)
```

Un uso particularmente útil del _slicing_ consiste en emplear un paso negativo para invertir el orden de la lista sin necesidad de invocar un método adicional: la sintaxis `lista[::-1]` recorre la lista completa desde el final hacia el principio, generando una nueva lista invertida.

```python
puertos = [21, 22, 23, 80, 443]
puertos_invertidos = puertos[::-1]   # [443, 80, 23, 22, 21]
```

Es importante remarcar que tanto la indexación simple como el _slicing_ **no modifican** la lista original: ambas operaciones devuelven un nuevo valor (un elemento individual en el primer caso, una nueva lista en el segundo), dejando intacta la lista de la que provienen, salvo que el resultado se reasigne explícitamente a la variable original.

### Listas Anidadas

Una lista puede contener otras listas como elementos, dando lugar a estructuras anidadas que permiten representar datos con varias dimensiones, como matrices o tablas. Este patrón resulta especialmente útil para representar, por ejemplo, los resultados de un escaneo de red en el que cada fila agrupa un host junto con la lista de sus puertos abiertos.

```python
# Lista anidada: cada elemento es a su vez una lista [host, [puertos_abiertos]]
escaneo = [
    ["192.168.1.10", [22, 80, 443]],
    ["192.168.1.11", [21, 23, 3389]],
]

# Para acceder a un elemento dentro de una lista anidada, se encadenan los índices
primer_host = escaneo[0][0]            # "192.168.1.10"
puertos_primer_host = escaneo[0][1]    # [22, 80, 443]
primer_puerto_primer_host = escaneo[0][1][0]   # 22
```

Cuando la estructura de datos a representar tiene un número fijo y conocido de filas y columnas, este mismo principio puede emplearse para construir una matriz, en la que cada fila es una lista de igual longitud:

```python
# Matriz 3x3 representando, por ejemplo, una grilla de estado de hosts (1=activo, 0=inactivo)
matriz_red = [
    [1, 0, 1],
    [0, 0, 1],
    [1, 1, 0],
]

# Acceso a la celda de la fila 1, columna 2
estado = matriz_red[1][2]   # 1
```

## Mutabilidad: Referencias, Copias y Aliasing

Un aspecto avanzado, pero crítico, del comportamiento de las listas en Python es que son objetos **mutables** manejados internamente por referencia. Esto implica que, cuando se asigna una lista existente a una nueva variable utilizando el operador `=`, no se crea una copia independiente de la lista, sino que ambas variables terminan apuntando al mismo objeto en memoria. En consecuencia, modificar la lista a través de una de las variables afecta también lo que se observa a través de la otra, un fenómeno conocido como _aliasing_.

```python
hosts_originales = ["192.168.1.10", "192.168.1.11"]
hosts_referenciados = hosts_originales   # NO es una copia, es la misma lista en memoria

hosts_referenciados.append("192.168.1.12")

print(hosts_originales)      # ['192.168.1.10', '192.168.1.11', '192.168.1.12']
print(hosts_referenciados)   # ['192.168.1.10', '192.168.1.11', '192.168.1.12']
```

Para obtener una copia independiente de una lista, de modo que las modificaciones sobre una no afecten a la otra, Python ofrece varias alternativas equivalentes para una copia superficial (_shallow copy_): el método `copy()`, el constructor `list()`, o el _slicing_ completo `[:]`.

```python
hosts_originales = ["192.168.1.10", "192.168.1.11"]
hosts_copiados = hosts_originales.copy()   # ahora sí es una copia independiente

hosts_copiados.append("192.168.1.12")

print(hosts_originales)   # ['192.168.1.10', '192.168.1.11']  (sin cambios)
print(hosts_copiados)     # ['192.168.1.10', '192.168.1.11', '192.168.1.12']
```

Es importante notar que estas formas de copia son "superficiales": si la lista original contiene a su vez otras listas anidadas, la copia superficial duplica la lista exterior, pero las listas internas siguen siendo las mismas referencias compartidas entre el original y la copia. Cuando se trabaja con estructuras anidadas y se necesita una independencia total entre la copia y el original, es necesario recurrir a una copia profunda (_deep copy_) mediante el módulo `copy` de la biblioteca estándar:

```python
import copy

escaneo_original = [["192.168.1.10", [22, 80]], ["192.168.1.11", [21, 23]]]
escaneo_copia_profunda = copy.deepcopy(escaneo_original)

escaneo_copia_profunda[0][1].append(443)

print(escaneo_original[0][1])        # [22, 80]       (no se vio afectado)
print(escaneo_copia_profunda[0][1])  # [22, 80, 443]
```

Comprender esta diferencia entre referencia, copia superficial y copia profunda resulta fundamental para evitar errores sutiles y difíciles de depurar, especialmente en scripts donde una misma estructura de datos se pasa como argumento entre varias funciones que la modifican.

## Operaciones con Listas

### Añadir Elementos: `append()`, `extend()` e `insert()`

El método `append()` agrega un único elemento al final de la lista, sin importar el tipo de dato que se le proporcione: si se le pasa otra lista como argumento, esta se añade como un único elemento anidado, no se combinan sus contenidos. El método `extend()`, en cambio, recibe un iterable (como otra lista) y agrega cada uno de sus elementos individualmente al final de la lista original, en lugar de anidarlo como un único bloque.

```python
puertos = [22, 80]

puertos.append(443)
print(puertos)   # [22, 80, 443]

puertos.append([445, 3389])
print(puertos)   # [22, 80, 443, [445, 3389]]   <- se agregó como UN elemento anidado

puertos = [22, 80, 443]
puertos.extend([445, 3389])
print(puertos)   # [22, 80, 443, 445, 3389]     <- se agregaron como elementos individuales
```

El método `insert()` permite agregar un elemento en una posición específica de la lista, desplazando automáticamente hacia la derecha a todos los elementos que ocupaban esa posición y las siguientes.

```python
puertos = [22, 443]
puertos.insert(1, 80)   # inserta el valor 80 en la posición de índice 1
print(puertos)   # [22, 80, 443]
```

### Eliminar Elementos: `remove()`, `pop()`, `clear()` y `del`

El método `remove()` elimina la **primera ocurrencia** de un valor específico dentro de la lista, basándose en su contenido y no en su posición; si el valor no existe en la lista, se produce un error de tipo `ValueError`. El método `pop()`, en cambio, elimina y devuelve el elemento ubicado en una posición determinada (por defecto, el último elemento de la lista si no se especifica un índice), lo cual lo hace especialmente útil cuando se necesita tanto eliminar como reutilizar el valor extraído.

```python
puertos = [22, 80, 443, 80]

puertos.remove(80)   # elimina solo la PRIMERA aparición del valor 80
print(puertos)   # [22, 443, 80]

ultimo_puerto = puertos.pop()       # elimina y devuelve el último elemento
print(ultimo_puerto)   # 80
print(puertos)          # [22, 443]

primer_puerto = puertos.pop(0)      # elimina y devuelve el elemento en el índice 0
print(primer_puerto)   # 22
```

El método `clear()` elimina la totalidad de los elementos de la lista, dejándola vacía pero conservando la misma referencia en memoria, lo cual es distinto de reasignar la variable a una lista nueva. La declaración `del`, por su parte, es una sentencia del lenguaje (no un método de la lista) que permite eliminar un elemento por su índice, un rango completo mediante _slicing_, o incluso eliminar la variable que referencia a la lista por completo.

```python
puertos = [22, 80, 443]

del puertos[0]      # elimina el elemento en el índice 0
print(puertos)   # [80, 443]

puertos.clear()      # vacía la lista por completo
print(puertos)   # []
```

### Ordenar Listas: `sort()` frente a `sorted()`

Python ofrece dos formas de ordenar una lista, que se diferencian fundamentalmente en si modifican la lista original o no. El método `sort()`, invocado directamente sobre la lista, la ordena **"in place"**, es decir, modifica la lista original y no devuelve un nuevo valor (devuelve `None`). La función incorporada `sorted()`, en cambio, recibe cualquier iterable como argumento y devuelve una **nueva lista** ordenada, sin alterar el iterable original.

```python
puertos = [443, 22, 3389, 80]

# sort(): modifica la lista original, no devuelve nada útil
puertos.sort()
print(puertos)   # [22, 80, 443, 3389]

# sorted(): devuelve una NUEVA lista, la original permanece intacta
puertos_originales = [443, 22, 3389, 80]
puertos_ordenados = sorted(puertos_originales)
print(puertos_originales)   # [443, 22, 3389, 80]   (sin cambios)
print(puertos_ordenados)    # [22, 80, 443, 3389]
```

Ambas formas admiten el parámetro `reverse=True` para ordenar en sentido descendente, así como el parámetro `key`, que recibe una función (frecuentemente una lambda) utilizada para definir el criterio de ordenamiento, tal como se vio en notas anteriores sobre funciones lambda combinadas con `sorted()`.

```python
hallazgos = [
    {"host": "192.168.1.10", "severidad": 7},
    {"host": "192.168.1.11", "severidad": 9},
]

# Ordenar de mayor a menor severidad usando una key personalizada
hallazgos.sort(key=lambda h: h["severidad"], reverse=True)
print(hallazgos)
```

En términos de buenas prácticas, conviene utilizar `sort()` cuando ya no se necesita preservar el orden original de la lista, y `sorted()` cuando se requiere conservar la lista original intacta para utilizarla en otra parte del programa.

### Invertir el Orden: `reverse()` frente a `[::-1]`

De forma análoga a lo que ocurre con `sort()` y `sorted()`, Python ofrece dos formas de invertir el orden de una lista con un comportamiento distinto respecto a la mutabilidad. El método `reverse()` invierte la lista **"in place"**, modificando la lista original directamente y sin devolver un nuevo valor. El _slicing_ `[::-1]`, en cambio, devuelve una **nueva lista** con los elementos en orden inverso, sin alterar la lista original.

```python
puertos = [22, 80, 443]

puertos.reverse()   # modifica la lista original
print(puertos)   # [443, 80, 22]

puertos_originales = [22, 80, 443]
puertos_invertidos = puertos_originales[::-1]   # genera una nueva lista
print(puertos_originales)   # [22, 80, 443]   (sin cambios)
print(puertos_invertidos)   # [443, 80, 22]
```

### Comprensión de Listas como Herramienta de Manipulación Avanzada

Tal como se desarrolló en profundidad en notas anteriores, la comprensión de listas constituye la forma "pythónica" por excelencia de crear y transformar listas de manera concisa, combinando en una sola expresión la iteración sobre una secuencia, una transformación opcional de cada elemento y un filtrado opcional mediante una cláusula `if`. Su dominio resulta indispensable para escribir código avanzado e idiomático en Python, y debe considerarse, en la mayoría de los casos, como la alternativa preferida frente a un bucle `for` tradicional combinado con `append()`, siempre que la lógica de transformación se mantenga razonablemente simple.

## Listas como Pilas y Colas

Más allá de sus métodos individuales, las listas pueden emplearse para implementar dos estructuras de datos abstractas fundamentales: la **pila** (_stack_) y, con ciertas reservas, la **cola** (_queue_). Estas estructuras no son exclusivas de Python ni de las listas en particular: se trata de patrones de acceso a datos presentes en prácticamente cualquier lenguaje de programación, y resultan especialmente relevantes en ciberseguridad porque modelan de forma natural algoritmos de recorrido y exploración que aparecen constantemente en herramientas de reconocimiento, _crawling_ y análisis de grafos de ataque.

### Pilas (LIFO) y Recorrido en Profundidad

Una pila sigue el principio LIFO (_Last In, First Out_: el último elemento en entrar es el primero en salir), y puede implementarse de forma natural con una lista utilizando `append()` para apilar elementos en el extremo final, y `pop()` (sin argumentos) para desapilar el último elemento agregado. Ambas operaciones tienen un costo computacional constante, `O(1)`, ya que actúan exclusivamente sobre el extremo final de la lista, sin necesidad de desplazar ningún otro elemento en memoria. Esto convierte a la pila en una estructura extremadamente eficiente siempre que las inserciones y eliminaciones se realicen únicamente en ese extremo.

python

```python
pila_urls_pendientes = []

pila_urls_pendientes.append("http://192.168.1.10/admin")
pila_urls_pendientes.append("http://192.168.1.10/login")
pila_urls_pendientes.append("http://192.168.1.10/api")

siguiente_url = pila_urls_pendientes.pop()   # extrae "http://192.168.1.10/api" (el último agregado)
print(siguiente_url)
```

El comportamiento LIFO de la pila es precisamente lo que la convierte en la estructura natural para implementar un recorrido en profundidad (_Depth-First Search_, DFS). Al explorar, por ejemplo, la estructura de directorios de una aplicación web mediante fuerza bruta, cada vez que se descubre un nuevo enlace o subdirectorio, este se apila junto al resto de los pendientes; al extraer el siguiente elemento a visitar, se obtiene siempre el descubrimiento más reciente, lo que hace que el algoritmo "profundice" primero por una rama completa de la estructura antes de retroceder a explorar las demás. Este mismo patrón resulta útil para implementar funcionalidades de deshacer (_undo_) en herramientas interactivas, donde cada acción realizada se apila, y deshacer la última acción consiste simplemente en desapilarla.

python

```python
# DFS simplificado: explorar rutas de un sitio web apilando los descubrimientos más recientes
pila_rutas = ["/"]
rutas_visitadas = []

while pila_rutas:
    ruta_actual = pila_rutas.pop()
    if ruta_actual in rutas_visitadas:
        continue

    rutas_visitadas.append(ruta_actual)
    print(f"Visitando: {ruta_actual}")

    # Simulación: cada ruta "descubre" nuevas subrutas, que se apilan para visitarse a continuación
    nuevas_rutas = {"/": ["/admin", "/login"], "/admin": ["/admin/panel"]}.get(ruta_actual, [])
    for nueva_ruta in nuevas_rutas:
        pila_rutas.append(nueva_ruta)
```

### Colas (FIFO) y Recorrido en Anchura

Si bien una lista también puede utilizarse para implementar una cola (FIFO, _First In, First Out_: el primer elemento en entrar es el primero en salir) mediante `append()` para encolar y `pop(0)` para desencolar, esta práctica no resulta eficiente para colas de gran tamaño. El motivo es que eliminar el primer elemento de una lista mediante `pop(0)` tiene un costo `O(n)`, ya que el intérprete debe desplazar en memoria, una posición hacia la izquierda, a todos los elementos restantes de la lista; en una cola que crece y se vacía constantemente, este costo se repite en cada operación, degradando notablemente el rendimiento a medida que aumenta la cantidad de elementos procesados.

Para implementar colas de forma eficiente, la biblioteca estándar de Python ofrece la estructura `deque` (doble cola, de _double-ended queue_) del módulo `collections`, diseñada específicamente para permitir inserciones y eliminaciones eficientes, con costo `O(1)`, tanto en el extremo final como en el extremo inicial de la colección.

python

```python
from collections import deque

cola_hosts_pendientes = deque(["192.168.1.10", "192.168.1.11", "192.168.1.12"])

cola_hosts_pendientes.append("192.168.1.13")   # encola al final, O(1)
siguiente_host = cola_hosts_pendientes.popleft()  # desencola desde el principio, O(1)

print(siguiente_host)            # 192.168.1.10
print(cola_hosts_pendientes)     # deque(['192.168.1.11', '192.168.1.12', '192.168.1.13'])
```

El comportamiento FIFO de la cola es el fundamento de los algoritmos de recorrido en anchura (_Breadth-First Search_, BFS), en los que se exploran primero todos los elementos descubiertos en un mismo "nivel" antes de avanzar al siguiente. Este enfoque resulta particularmente apropiado, por ejemplo, al mapear una red por capas de cercanía a partir de un host inicial: primero se procesan todos los hosts directamente conectados al punto de partida, y solo después se avanza hacia los hosts descubiertos a través de ellos, lo que permite construir progresivamente un mapa de la red ordenado por distancia respecto al punto de entrada.

python

```python
# BFS simplificado: explorar una red por niveles de cercanía usando una cola
cola = deque(["192.168.1.1"])
visitados = set()

# Topología simulada: qué hosts son alcanzables desde cada host
topologia = {
    "192.168.1.1": ["192.168.1.2", "192.168.1.3"],
    "192.168.1.2": ["192.168.1.4"],
}

while cola:
    host_actual = cola.popleft()
    if host_actual in visitados:
        continue

    visitados.add(host_actual)
    print(f"Host alcanzado: {host_actual}")

    for host_vecino in topologia.get(host_actual, []):
        cola.append(host_vecino)
```

Vale la pena mencionar que, además de `deque`, la biblioteca estándar ofrece la clase `Queue` del módulo `queue`, pensada específicamente para escenarios de concurrencia con múltiples hilos: a diferencia de una lista o de un `deque` simple, `Queue` incorpora mecanismos internos de bloqueo (_locking_) que garantizan que varios hilos puedan encolar y desencolar elementos de forma segura sin generar condiciones de carrera. Esta estructura resulta especialmente relevante al diseñar herramientas de escaneo concurrente, donde múltiples hilos trabajadores consumen objetivos de una misma cola compartida.

## Buenas Prácticas en el Uso de Listas

A la hora de trabajar con listas en proyectos reales, conviene tener presentes algunas recomendaciones que favorecen tanto la legibilidad como el rendimiento del código. En primer lugar, resulta preferible utilizar comprensión de listas en lugar de un bucle `for` con `append()` siempre que la transformación a realizar sea simple, reservando el bucle tradicional para lógicas más complejas que perjudicarían la legibilidad si se forzaran dentro de una comprensión.

En segundo lugar, es importante recordar la diferencia entre operaciones que modifican la lista original (`append()`, `extend()`, `insert()`, `remove()`, `pop()`, `sort()`, `reverse()`) y aquellas que devuelven una nueva lista sin alterar la original (`sorted()`, el _slicing_ `[::-1]`, las comprensiones de listas). Confundir ambos comportamientos es una fuente habitual de errores, especialmente al encadenar operaciones o al asumir erróneamente que un método como `sort()` devuelve la lista ordenada, cuando en realidad devuelve `None`.

En tercer lugar, dado que las listas son objetos mutables manejados por referencia, se debe prestar especial atención al pasar una lista como argumento a una función: si dicha función la modifica internamente (por ejemplo, mediante `append()`), el cambio se reflejará también en la lista original fuera de la función, lo cual puede ser el comportamiento deseado o una fuente de errores difíciles de rastrear, según el caso. Cuando se desea evitar este efecto, conviene trabajar sobre una copia explícita de la lista, ya sea mediante `copy()` o `copy.deepcopy()` según corresponda.

Finalmente, en cuanto a rendimiento, conviene tener en cuenta que `append()` es una operación eficiente (de costo prácticamente constante), mientras que `insert()` en posiciones distintas del final, así como `pop(0)` o `del lista[0]`, son operaciones costosas en listas grandes, ya que requieren desplazar en memoria a todos los elementos restantes. Cuando un script de ciberseguridad necesita procesar estructuras de datos de gran tamaño, como resultados masivos de escaneos de red completos o diccionarios extensos de contraseñas, esta diferencia de rendimiento puede volverse un factor determinante, y en esos casos puede resultar más adecuado recurrir a estructuras alternativas como `deque` o directamente a generadores, que procesan los datos de forma perezosa sin necesidad de mantener toda la colección en memoria simultáneamente.