# Conjuntos (_Sets_): Estructura, Operaciones y Buenas Prácticas

## Introducción

Los conjuntos son una colección de elementos sin orden definido y sin elementos repetidos, inspirados directamente en la teoría de conjuntos de las matemáticas. A diferencia de las listas y las tuplas, cuyo valor principal radica en preservar un orden y permitir duplicados, los conjuntos están diseñados específicamente para gestionar colecciones de elementos únicos y para resolver operaciones de comparación entre colecciones —como uniones, intersecciones y diferencias— de forma directa y altamente eficiente. En el contexto de la ciberseguridad, esta naturaleza los convierte en la estructura natural para tareas como deduplicar listas de IOCs (_Indicators of Compromise_) provenientes de múltiples fuentes, comparar listados de puertos o hosts entre distintos escaneos, o mantener listas de bloqueo (_blacklists_) que requieren verificaciones de pertenencia extremadamente rápidas.

## Características de los Conjuntos

### Unicidad

Los conjuntos descartan automáticamente cualquier elemento duplicado en el momento en que este se intenta agregar, sin que esto produzca un error: simplemente, si el elemento ya existe en el conjunto, la operación de adición no tiene ningún efecto adicional. Esta característica los vuelve la herramienta natural para garantizar que una colección de datos no contenga repeticiones.

```python
ips_detectadas = {"192.168.1.10", "192.168.1.11", "192.168.1.10", "192.168.1.12"}
print(ips_detectadas)   # {'192.168.1.10', '192.168.1.11', '192.168.1.12'}  (el duplicado se descartó solo)
```

### Desordenados

A diferencia de las listas y las tuplas, los conjuntos no garantizan ningún orden específico para sus elementos. Internamente, un conjunto se implementa mediante una tabla hash, una estructura optimizada para verificar rápidamente si un valor está presente, pero que no conserva ninguna noción de secuencia ni de posición. Como consecuencia directa de esto, los conjuntos no admiten indexación ni _slicing_: no existe un "primer elemento" ni un "elemento en la posición 2" al que se pueda acceder mediante corchetes, como sí ocurre con listas y tuplas.

```python
puertos_unicos = {443, 22, 80, 21}

# print(puertos_unicos[0])   # TypeError: 'set' object is not subscriptable
```

### Mutabilidad (con una Restricción Importante)

Un conjunto, como objeto, es mutable: es posible agregar y eliminar elementos después de su creación. Sin embargo, esta mutabilidad se aplica al conjunto en sí, no a sus elementos individuales, los cuales deben ser, obligatoriamente, de un tipo inmutable y _hashable_. Esto significa que un conjunto puede contener números, cadenas, booleanos o tuplas (siempre que estas, a su vez, solo contengan elementos inmutables), pero **no puede contener listas, diccionarios ni otros conjuntos**, ya que estos tipos son mutables y, por lo tanto, no son _hashables_. Este requisito está directamente relacionado con el funcionamiento interno de la tabla hash que sustenta a los conjuntos, la cual necesita que cada elemento tenga un valor de hash estable a lo largo de su vida útil dentro de la colección.

```python
hosts_objetivo = {"192.168.1.10", ("192.168.1.11", 22)}   # cadenas y tuplas: válido, son inmutables

# puertos_invalido = {[22, 80], [443]}   # TypeError: unhashable type: 'list'
```

## Operaciones con Conjuntos

### Adición y Eliminación de Elementos

El método `add()` incorpora un único elemento al conjunto; si dicho elemento ya estaba presente, la operación no produce ningún efecto ni error. Para eliminar un elemento existen dos métodos con un comportamiento distinto ante la ausencia del valor: `remove()` elimina el elemento indicado y lanza un `KeyError` si este no se encuentra en el conjunto, mientras que `discard()` realiza la misma eliminación pero, si el elemento no existe, simplemente no hace nada, sin generar ningún error. El método `pop()`, por su parte, elimina y devuelve un elemento arbitrario del conjunto (dado que los conjuntos no tienen orden, no es posible predecir cuál será), y `clear()` elimina la totalidad de los elementos, dejando el conjunto vacío.

```python
ips_bloqueadas = {"185.220.101.5", "194.165.16.3"}

ips_bloqueadas.add("91.243.85.17")
print(ips_bloqueadas)

ips_bloqueadas.discard("10.0.0.1")   # no existe en el conjunto, pero no genera error
ips_bloqueadas.remove("194.165.16.3")   # sí existe, se elimina sin problemas

# ips_bloqueadas.remove("10.0.0.1")   # esto SÍ lanzaría un KeyError, porque ya no usamos discard()
```

Esta diferencia entre `remove()` y `discard()` resulta especialmente relevante a la hora de decidir cuál utilizar: `discard()` es la opción más segura cuando no se tiene certeza de que el elemento a eliminar realmente esté presente en el conjunto, evitando así tener que envolver la operación en un bloque `try`/`except` únicamente para contemplar esa posibilidad.

### Operaciones Matemáticas de Conjuntos

La verdadera potencia de los conjuntos reside en las operaciones que reproducen directamente la teoría de conjuntos matemática, disponibles tanto como métodos con nombre explícito como mediante operadores simbólicos equivalentes.

La **unión** combina los elementos de dos conjuntos en uno solo, sin duplicados, y puede obtenerse mediante el método `union()` o el operador `|`. Resulta útil, por ejemplo, para consolidar listas de hosts detectados por distintas herramientas de escaneo en un único conjunto sin repeticiones.

```python
hosts_nmap = {"192.168.1.10", "192.168.1.11", "192.168.1.12"}
hosts_masscan = {"192.168.1.11", "192.168.1.13"}

todos_los_hosts = hosts_nmap | hosts_masscan   # equivalente a hosts_nmap.union(hosts_masscan)
print(todos_los_hosts)   # {'192.168.1.10', '192.168.1.11', '192.168.1.12', '192.168.1.13'}
```

La **intersección** devuelve únicamente los elementos presentes en ambos conjuntos simultáneamente, y se obtiene mediante el método `intersection()` o el operador `&`. Esta operación resulta particularmente valiosa para identificar coincidencias entre dos fuentes de datos, como hallar qué hosts fueron detectados por dos herramientas distintas, lo que suele aumentar la confianza en ese hallazgo.

```python
hosts_confirmados = hosts_nmap & hosts_masscan   # equivalente a hosts_nmap.intersection(hosts_masscan)
print(hosts_confirmados)   # {'192.168.1.11'}   <- detectado por AMBAS herramientas
```

La **diferencia** devuelve los elementos que están presentes en el primer conjunto pero no en el segundo, y se obtiene mediante el método `difference()` o el operador `-`. Esta operación es extremadamente útil para detectar elementos exclusivos de una fuente, como identificar qué hosts fueron detectados por una herramienta pero pasados por alto por otra, lo cual puede señalar una limitación en la cobertura de esta última.

```python
solo_nmap = hosts_nmap - hosts_masscan   # equivalente a hosts_nmap.difference(hosts_masscan)
print(solo_nmap)   # {'192.168.1.10', '192.168.1.12'}   <- detectados solo por nmap
```

La **diferencia simétrica** devuelve los elementos que pertenecen a uno de los dos conjuntos, pero no a ambos a la vez (es decir, excluye la intersección), y se obtiene mediante el método `symmetric_difference()` o el operador `^`. Resulta útil para detectar discrepancias totales entre dos fuentes de datos, agrupando en un solo resultado tanto lo que falta en una como lo que falta en la otra.

```python
discrepancias = hosts_nmap ^ hosts_masscan   # equivalente a hosts_nmap.symmetric_difference(hosts_masscan)
print(discrepancias)   # {'192.168.1.10', '192.168.1.12', '192.168.1.13'}
```

### Relaciones entre Conjuntos: Subconjuntos y Superconjuntos

Más allá de combinar conjuntos, Python permite consultar directamente las relaciones lógicas que existen entre ellos. El método `issubset()` (o el operador `<=`) verifica si todos los elementos de un conjunto están contenidos dentro de otro, mientras que `issuperset()` (o el operador `>=`) verifica la relación inversa: si un conjunto contiene a todos los elementos de otro. El método `isdisjoint()` verifica si dos conjuntos no comparten ningún elemento en común, es decir, si su intersección está vacía.

```python
puertos_criticos = {21, 23, 445, 3389}
puertos_detectados = {21, 22, 23, 80, 443, 445, 3389}

# ¿Todos los puertos críticos están entre los detectados?
print(puertos_criticos.issubset(puertos_detectados))   # True
print(puertos_criticos <= puertos_detectados)          # equivalente

puertos_aislados = {9999, 8888}
print(puertos_detectados.isdisjoint(puertos_aislados))   # True, no comparten ningún elemento
```

### Pruebas de Pertenencia y su Ventaja de Rendimiento

Comprobar si un elemento pertenece a un conjunto se realiza con el operador `in`, exactamente igual que con listas y tuplas. Sin embargo, existe una diferencia de rendimiento sustancial entre verificar pertenencia en un conjunto frente a hacerlo en una lista: gracias a su implementación interna basada en una tabla hash, comprobar si un elemento pertenece a un conjunto tiene un costo computacional promedio constante, `O(1)`, independientemente del tamaño del conjunto. En contraste, esa misma verificación sobre una lista requiere, en el peor de los casos, recorrerla por completo, con un costo `O(n)` que crece de forma proporcional a la cantidad de elementos.

```python
import time

# Comparación ilustrativa de rendimiento: lista vs. set para verificar pertenencia
ips_maliciosas_lista = [f"10.0.{i}.{j}" for i in range(256) for j in range(256)]
ips_maliciosas_set = set(ips_maliciosas_lista)

ip_a_verificar = "10.0.255.255"   # peor caso: está al final de la lista

inicio = time.perf_counter()
resultado_lista = ip_a_verificar in ips_maliciosas_lista
tiempo_lista = time.perf_counter() - inicio

inicio = time.perf_counter()
resultado_set = ip_a_verificar in ips_maliciosas_set
tiempo_set = time.perf_counter() - inicio

print(f"Verificación en lista: {tiempo_lista:.8f} seg")
print(f"Verificación en set:   {tiempo_set:.8f} seg")
```

Esta diferencia de rendimiento se vuelve crítica al trabajar con colecciones de gran tamaño, como una lista de decenas de miles de direcciones IP maliciosas conocidas: utilizar un conjunto en lugar de una lista para realizar estas verificaciones puede significar la diferencia entre un script que responde instantáneamente y uno que se vuelve notablemente lento a medida que la lista de referencia crece.

### `frozenset`: Conjuntos Inmutables

Python ofrece, además del tipo `set` mutable visto hasta ahora, una variante inmutable denominada `frozenset`. Una vez creado, un `frozenset` no admite la adición ni eliminación de elementos, de forma análoga a como una tupla es la versión inmutable de una lista. Esta inmutabilidad tiene una consecuencia directa relevante: al ser inmutable y, por lo tanto, _hashable_, un `frozenset` sí puede utilizarse como elemento dentro de otro conjunto, o como clave de un diccionario, algo que un `set` mutable tiene prohibido por las mismas razones discutidas previamente respecto a los elementos internos de un conjunto.

```python
permisos_lectura = frozenset({"read", "list"})
permisos_escritura = frozenset({"read", "write", "list"})

# Un frozenset SÍ puede usarse como clave de diccionario o como elemento de otro conjunto
politicas_conocidas = {permisos_lectura, permisos_escritura}

# permisos_lectura.add("write")   # AttributeError: 'frozenset' object has no attribute 'add'
```

El uso de `frozenset` resulta apropiado cuando se necesita representar un conjunto de valores fijo que, además, debe poder anidarse dentro de otra estructura que exija que sus elementos sean _hashables_, como ocurre al modelar conjuntos de permisos o capacidades predefinidas que luego se agrupan o comparan entre sí.

### Comprensión de Conjuntos (_Set Comprehensions_)

De forma análoga a la comprensión de listas, Python admite la comprensión de conjuntos, utilizando llaves `{}` en lugar de corchetes. Esta construcción genera directamente un conjunto a partir de una secuencia, aplicando opcionalmente una transformación y un filtro, y deduplicando automáticamente cualquier resultado repetido como consecuencia natural de tratarse de un conjunto.

```python
correos_extraidos = ["admin@empresa.com", "soporte@empresa.com", "ADMIN@empresa.com", "admin@empresa.com"]

# Comprensión de conjuntos: normaliza a minúsculas y deduplica en un solo paso
dominios_unicos = {correo.split("@")[1].lower() for correo in correos_extraidos}
print(dominios_unicos)   # {'empresa.com'}
```

## Uso de Conjuntos en Python

### Eliminación de Duplicados

La aplicación más inmediata de los conjuntos consiste en garantizar que una colección de datos no contenga elementos repetidos. La forma más directa de deduplicar una lista existente es, simplemente, convertirla en un conjunto mediante el constructor `set()`, y volver a convertirla en lista si se necesita preservar el tipo de dato original.

```python
hosts_con_duplicados = ["192.168.1.10", "192.168.1.11", "192.168.1.10", "192.168.1.12", "192.168.1.11"]

hosts_unicos = list(set(hosts_con_duplicados))
print(hosts_unicos)
```

Es importante señalar que esta conversión no preserva el orden original de los elementos, ya que los conjuntos son desordenados. Cuando preservar el orden original resulta importante, conviene recurrir, en su lugar, a la técnica vista en notas anteriores basada en `dict.fromkeys()`, que deduplica conservando el orden de la primera aparición de cada elemento.

### Relaciones entre Colecciones

Las operaciones de conjuntos descritas anteriormente —unión, intersección, diferencia y diferencia simétrica— constituyen una herramienta extremadamente expresiva para razonar sobre relaciones entre distintas colecciones de datos, una necesidad recurrente al correlacionar resultados provenientes de múltiples fuentes en un proceso de reconocimiento: comparar los puertos abiertos detectados en dos escaneos realizados en distintos momentos, identificar qué hosts de una red interna nunca fueron analizados, o determinar qué direcciones IP de una lista de IOCs ya habían sido vistas en escaneos anteriores.

### Rendimiento en Búsquedas sobre Grandes Volúmenes de Datos

Como se desarrolló en profundidad anteriormente, los conjuntos ofrecen un rendimiento de búsqueda muy superior al de listas y tuplas para verificaciones de pertenencia, gracias a su implementación basada en tablas hash. Esta característica los convierte en la estructura de elección al implementar listas de bloqueo, listas blancas, o cualquier mecanismo que deba consultar con frecuencia si un valor determinado pertenece a un conjunto de referencia potencialmente extenso.

## Buenas Prácticas en el Uso de Conjuntos

Al decidir entre utilizar un conjunto o una lista, conviene aplicar un criterio claro: si el orden de los elementos no es relevante para el problema, si no se necesitan elementos duplicados, y si la operación principal a realizar sobre la colección es verificar pertenencia o compararla con otra colección, un conjunto es casi siempre la estructura más adecuada, tanto por claridad de intención como por rendimiento. Si, en cambio, el orden de los elementos importa, o se necesita acceder a ellos por posición mediante un índice, una lista sigue siendo la opción correcta.

También conviene preferir `discard()` sobre `remove()` cuando no existe certeza absoluta de que el elemento a eliminar esté presente en el conjunto, evitando así tener que manejar explícitamente la excepción `KeyError` que `remove()` produciría en ese caso. De forma relacionada, al construir conjuntos que eventualmente deban anidarse dentro de otras estructuras (como otro conjunto o un diccionario), es importante recordar la restricción de _hashabilidad_: si se necesita un conjunto de conjuntos, o un conjunto utilizado como clave, la herramienta correcta es `frozenset`, no un `set` mutable estándar.

Finalmente, al trabajar con grandes volúmenes de datos en los que las verificaciones de pertenencia son frecuentes —como listas extensas de IOCs, direcciones IP maliciosas conocidas o hashes de malware—, conviene evaluar siempre la conversión de esas colecciones a conjuntos desde el inicio, en lugar de mantenerlas como listas, ya que el costo único de esa conversión suele verse ampliamente compensado por la mejora de rendimiento obtenida en cada verificación de pertenencia posterior, especialmente cuando dicha verificación se repite muchas veces a lo largo de la ejecución del script.