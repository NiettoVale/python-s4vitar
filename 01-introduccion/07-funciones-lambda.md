# Funciones Lambda (Funciones Anónimas) en Python

## Concepto

Las funciones lambda, también conocidas como funciones anónimas, reciben este nombre porque, a diferencia de las funciones definidas con `def`, no requieren que se les asigne un nombre explícito en el momento de su creación. Su propósito principal es permitir la creación de pequeñas funciones directamente en el lugar donde se necesitan, generalmente destinadas a resolver una operación puntual y breve, sin la necesidad de declarar formalmente una función independiente en otra parte del código.

En Python, una función lambda se define utilizando la palabra clave `lambda`, seguida de una lista de argumentos separados por comas, dos puntos, y finalmente la expresión que se desea evaluar y devolver. A diferencia de una función tradicional, una lambda no admite múltiples sentencias ni bloques de código extensos: su cuerpo se limita a una única expresión, cuyo resultado se devuelve de forma implícita, sin necesidad de utilizar la palabra clave `return`.

```python
# Sintaxis general de una función lambda
# lambda argumentos: expresión

saludo = lambda: "¡Hola Mundo!"
print(saludo())   # ¡Hola Mundo!

cuadrado = lambda numero: numero ** 2
print(cuadrado(2))   # 4

suma = lambda x, y: x + y
print(suma(7, 3))   # 10
```

Aunque en los ejemplos anteriores las funciones lambda fueron asignadas a una variable, es importante destacar que esto no es su uso más característico: su verdadero valor se manifiesta cuando se definen "al vuelo", como argumento directo de otra función, sin necesidad de almacenarlas en una variable previa.

## Ventajas y Limitaciones

La principal ventaja de las funciones lambda radica en su simplicidad sintáctica: permiten expresar una operación breve en una única línea, evitando la verbosidad que implicaría definir una función completa con `def` únicamente para resolver una tarea puntual que, además, probablemente no vaya a reutilizarse en otra parte del programa. Esta concisión resulta especialmente conveniente cuando se trabaja con funciones de orden superior, es decir, funciones que reciben otra función como argumento.

No obstante, esta misma simplicidad implica también ciertas limitaciones. Al estar restringidas a una única expresión, las funciones lambda no resultan adecuadas para lógicas que requieran múltiples pasos, estructuras condicionales complejas, manejo de excepciones o documentación mediante _docstrings_. En estos casos, sigue siendo preferible recurrir a una función definida con `def`, ya que forzar una lógica compleja dentro de una lambda tiende a perjudicar la legibilidad del código en lugar de mejorarla.

## Usos Comunes de las Funciones Lambda

### Funciones de Orden Superior

Las funciones lambda se utilizan con particular frecuencia junto a funciones de orden superior, es decir, funciones que aceptan otra función como uno de sus argumentos. Los ejemplos más representativos en Python son `map()`, `filter()` y `sorted()`, que adquieren gran parte de su utilidad práctica precisamente al combinarse con funciones lambda definidas en línea.

### Operaciones Simples

Las funciones lambda resultan ideales para realizar cálculos o transformaciones breves, en los casos donde escribir una función completa con `def` resultaría innecesariamente extenso en relación con la simplicidad de la operación que se desea resolver.

### Funcionalidad en Línea

Cuando se necesita una funcionalidad puntual, que no será reutilizada en ningún otro punto del programa, definir una función lambda directamente en el lugar donde se la utiliza evita la sobrecarga de declarar y nombrar una función independiente cuyo único propósito es ser invocada una sola vez.

## Funciones Lambda Combinadas con `map()` y `filter()`

Uno de los escenarios más habituales en los que se emplean funciones lambda es en combinación con `map()` y `filter()` para procesar listas de datos, un patrón que aparece con frecuencia en scripts de ciberseguridad orientados al procesamiento de resultados de escaneos, listas de objetivos o registros de eventos.

```python
puertos = [21, 22, 23, 80, 443, 445, 3389]

# map(): aplicar una transformación a cada elemento de la lista
# En este caso, generar el cuadrado de cada puerto (ejemplo ilustrativo)
cuadrados = list(map(lambda x: x ** 2, puertos))
print(cuadrados)

# filter(): conservar únicamente los elementos que cumplen una condición
# En este caso, conservar solo los puertos pares
pares = list(filter(lambda x: x % 2 == 0, puertos))
print(pares)
```

Un caso de uso más representativo del contexto de ciberseguridad consiste en utilizar `filter()` con una función lambda para extraer únicamente aquellos puertos considerados críticos dentro de una lista de resultados de escaneo, evitando así definir una función auxiliar independiente para una validación tan breve:

```python
puertos_detectados = [21, 22, 23, 80, 443, 445, 3389]
puertos_criticos = [21, 23, 445, 3389]

# Filtrar, mediante una lambda, los puertos que se consideran críticos
hallazgos_criticos = list(filter(lambda p: p in puertos_criticos, puertos_detectados))
print(hallazgos_criticos)   # [21, 23, 445, 3389]
```

## Funciones Lambda Combinadas con `sorted()`

La función `sorted()` admite un parámetro `key`, que permite indicar el criterio según el cual deben ordenarse los elementos de una secuencia. Este parámetro `key` espera recibir una función, lo que convierte a las lambdas en una herramienta especialmente adecuada para definir criterios de ordenamiento personalizados sin necesidad de declarar una función independiente.

```python
# Ordenar una lista de hallazgos (diccionarios) según su nivel de severidad numérica
hallazgos = [
    {"host": "192.168.1.10", "puerto": 22, "severidad": 7},
    {"host": "192.168.1.11", "puerto": 21, "severidad": 9},
    {"host": "192.168.1.12", "puerto": 80, "severidad": 4},
]

# La lambda indica que el criterio de orden es el valor asociado a la clave "severidad"
hallazgos_ordenados = sorted(hallazgos, key=lambda h: h["severidad"], reverse=True)

for hallazgo in hallazgos_ordenados:
    print(f"{hallazgo['host']}:{hallazgo['puerto']} -> severidad {hallazgo['severidad']}")
```

En este ejemplo, ordenar la lista de hallazgos de mayor a menor severidad mediante una función `def` independiente requeriría definir una función auxiliar de una sola línea cuyo único propósito sería extraer el valor de severidad de cada diccionario; la lambda permite expresar exactamente esa misma lógica de forma más directa y en el mismo punto donde se la utiliza.
