# Operadores Básicos, Operaciones con Secuencias y Conversión de Tipos en Python

## Operadores Aritméticos

Los operadores aritméticos son símbolos que Python utiliza para realizar cálculos matemáticos sobre valores numéricos. Aunque su uso principal está orientado a números, varios de estos operadores presentan un comportamiento particular al aplicarse sobre cadenas y listas, lo cual constituye una de las características distintivas del lenguaje.

El operador de **suma** (`+`) realiza la operación matemática esperada entre números, pero también admite un uso adicional sobre secuencias como cadenas y listas: en estos casos, no suma valores numéricos, sino que une ambas secuencias, generando una nueva secuencia que resulta de la combinación de las dos originales.

El operador de **resta** (`-`) se emplea exclusivamente para sustraer un número de otro. A diferencia de la suma, no tiene un significado definido cuando se aplica directamente sobre cadenas o listas, por lo que su uso queda restringido al ámbito numérico.

El operador de **multiplicación** (`*`) calcula el producto entre dos números, pero, al igual que la suma, adquiere un comportamiento especial al combinarse con cadenas o listas: en estos casos, repite el contenido de la secuencia tantas veces como indique el número entero proporcionado.

El operador de **división** (`/`) divide un número entre otro, devolviendo siempre como resultado un valor de tipo flotante, incluso cuando ambos operandos son números enteros y la división es exacta. Este comportamiento es propio de Python 3, y constituye una de las diferencias señaladas previamente respecto a Python 2.

El operador de **exponenciación** (`**`) eleva un número a la potencia indicada por el segundo operando. Por ejemplo, la expresión `2 ** 3` produce como resultado `8`. Este operador, a diferencia de la suma y la multiplicación, no tiene un comportamiento definido al aplicarse sobre cadenas o listas.

El operador **módulo** (`%`) devuelve el resto de la división entre dos números, en lugar del cociente. Resulta especialmente útil para determinar si un número es divisible por otro (cuando el resto es cero), así como para distribuir elementos de forma cíclica entre un conjunto de grupos o categorías. En el ámbito de la ciberseguridad, este operador aparece con frecuencia al repartir tareas de forma equitativa entre varios hilos o procesos, o al detectar patrones numéricos dentro de un conjunto de datos.

```python
# Operadores aritméticos básicos
intentos_totales = 3 + 2          # suma: 5
intentos_restantes = 10 - 4       # resta: 6
total_combinaciones = 4 * 3       # multiplicación: 12
promedio_tiempo = 7 / 2           # división: 3.5 (siempre devuelve float)
espacio_claves = 2 ** 8           # exponenciación: 256 (ej. combinaciones de un byte)
resto_reparto = 17 % 5            # módulo: 2 (resto de dividir 17 entre 5)
```

```python
# Uso práctico del operador módulo: repartir una lista de hosts entre 3 workers
hosts = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5"]
cantidad_workers = 3

for indice, host in enumerate(hosts):
    worker_asignado = indice % cantidad_workers
    print(f"Host {host} asignado al worker {worker_asignado}")
```

## Operaciones con Cadenas

Las cadenas, al ser secuencias de caracteres, admiten el uso de los operadores de suma y multiplicación con un significado adaptado a su naturaleza textual.

La **concatenación**, realizada mediante el operador `+`, permite unir varias cadenas en una sola. Esta operación resulta especialmente útil al construir mensajes dinámicos, rutas de archivos o cadenas de conexión a partir de fragmentos de información obtenidos durante la ejecución de un script.

```python
# Concatenación de cadenas para construir una URL de prueba
protocolo = "http://"
host = "192.168.1.10"
puerto = ":8080"

url_objetivo = protocolo + host + puerto
print(url_objetivo)   # http://192.168.1.10:8080
```

La **repetición**, realizada mediante el operador `*`, genera una nueva cadena compuesta por la cadena original repetida un número determinado de veces. Aunque su aplicación más habitual es de carácter ilustrativo, en un contexto de ciberseguridad puede emplearse, por ejemplo, para generar rápidamente cadenas de prueba de longitud arbitraria, útiles en pruebas de *buffer overflow* o de validación de campos de entrada.

```python
# Generación de una cadena de prueba para análisis de longitud de buffer
payload_prueba = "A" * 20
print(payload_prueba)   # AAAAAAAAAAAAAAAAAAAA
```

## Operaciones con Listas

Las listas, en tanto colecciones ordenadas y mutables, también admiten los operadores de suma y multiplicación, con un comportamiento análogo al observado en las cadenas.

La **concatenación** de listas mediante el operador `+` combina dos listas existentes en una nueva lista que contiene los elementos de ambas, preservando el orden original de cada una. Esta operación resulta útil, por ejemplo, al fusionar resultados provenientes de distintas fuentes de reconocimiento.

```python
# Concatenación de listas: combinar puertos detectados por dos herramientas distintas
puertos_nmap = [22, 80, 443]
puertos_masscan = [21, 8080]

puertos_totales = puertos_nmap + puertos_masscan
print(puertos_totales)   # [22, 80, 443, 21, 8080]
```

La **repetición** de listas mediante el operador `*` genera una nueva lista en la que todos los elementos de la lista original se repiten el número de veces indicado. Si bien su uso directo es menos frecuente en tareas de ciberseguridad, resulta de utilidad para inicializar rápidamente estructuras de datos de tamaño predefinido.

```python
# Inicialización de una lista de estados, uno por cada host a verificar
estados_iniciales = [False] * 5
print(estados_iniciales)   # [False, False, False, False, False]
```

## Funciones Especiales para Trabajar con Listas

### La Función `zip()`

La función `zip()` toma dos o más listas (u otros iterables) y las combina elemento a elemento, generando una secuencia de tuplas en la que cada tupla agrupa los valores que ocupan la misma posición en las listas originales. Esta función resulta especialmente útil cuando se dispone de varias listas relacionadas entre sí y se necesita procesarlas en conjunto, como ocurre al asociar una lista de hosts con una lista de puertos correspondientes.

```python
# Asociar cada host con su puerto abierto correspondiente mediante zip()
hosts = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
puertos = [22, 80, 443]

for host, puerto in zip(hosts, puertos):
    print(f"Host {host} -> puerto abierto {puerto}")
```

### La Función `map()`

La función `map()` aplica una función específica a cada uno de los elementos de un iterable, devolviendo un nuevo objeto con los resultados transformados. Esta función resulta de gran utilidad para normalizar o transformar datos en bloque, sin necesidad de escribir explícitamente un bucle `for` para cada caso.

```python
# Convertir una lista de puertos en formato string a enteros utilizando map()
puertos_texto = ["22", "80", "443"]
puertos_enteros = list(map(int, puertos_texto))

print(puertos_enteros)         # [22, 80, 443]
print(type(puertos_enteros[0]))  # <class 'int'>
```

## TypeCast: Conversión de Tipos de Datos

El *TypeCast*, o conversión de tipo, es el proceso mediante el cual se transforma el valor de una variable desde un tipo de dato hacia otro distinto. En Python, esta conversión se realiza de manera directa, utilizando el nombre del tipo de dato deseado como si fuera una función a la que se le pasa el valor a convertir como argumento.

Las conversiones más habituales incluyen el uso de `int()` para convertir una cadena numérica en un valor entero, `float()` para convertirla en un valor flotante, y `str()` para transformar un número (u otro tipo de dato) en su representación como cadena de texto.

```python
# Conversión de tipos: typecast
puerto_texto = "443"
puerto_numero = int(puerto_texto)        # de str a int

tiempo_respuesta_texto = "0.348"
tiempo_respuesta = float(tiempo_respuesta_texto)  # de str a float

intentos = 5
mensaje = "Intentos realizados: " + str(intentos)  # de int a str

print(puerto_numero, type(puerto_numero))
print(tiempo_respuesta, type(tiempo_respuesta))
print(mensaje)
```

Esta capacidad de conversión resulta particularmente relevante en scripts de ciberseguridad, donde con frecuencia se recibe información en formato de texto, por ejemplo desde la salida de una herramienta externa, un archivo de log o un argumento de línea de comandos, y resulta necesario convertirla a un tipo numérico para poder realizar comparaciones, cálculos o validaciones, o bien estandarizar distintos tipos de datos antes de almacenarlos en una misma estructura.

## String Formatting

Python ofrece varias técnicas para formatear cadenas de texto, permitiendo insertar el valor de variables dentro de ellas, así como controlar aspectos como el espaciado, la alineación y la precisión con la que se muestran los datos. A lo largo de la evolución del lenguaje han coexistido tres enfoques principales para resolver esta tarea, cada uno con un nivel distinto de legibilidad y flexibilidad.

### Operador `%` (Interpolación de Cadenas)

El operador `%` aplicado sobre cadenas constituye el método de formateo más clásico de Python, heredado en gran medida de la sintaxis de formateo del lenguaje C. Este método se conoce como *interpolación de cadenas*, y funciona insertando marcadores de posición dentro de la cadena que indican el tipo de dato esperado en cada posición: `%s` para cadenas de texto, `%d` para números enteros, y `%f` para números de punto flotante. Los valores a insertar se proporcionan a continuación de la cadena, también utilizando el operador `%`.

```python
# Interpolación de cadenas con el operador %
host = "192.168.1.10"
puerto = 443
tiempo_respuesta = 0.348

print("Host: %s - Puerto: %d - Tiempo: %f seg" % (host, puerto, tiempo_respuesta))
# Host: 192.168.1.10 - Puerto: 443 - Tiempo: 0.348000 seg
```

Si bien este método sigue siendo válido y puede encontrarse con frecuencia en código heredado, en la actualidad se considera una técnica menos legible y más propensa a errores que las alternativas más modernas, especialmente cuando se trabaja con un número elevado de variables a insertar.

### Método `format()`

Introducido en Python 2.6, el método `format()` permite una mayor flexibilidad y claridad respecto al operador `%`. En este caso, la cadena incluye marcadores de posición delimitados por llaves `{}`, que pueden dejarse vacíos para que los valores se inserten en el orden en que se proporcionan, o bien incluir un índice o un nombre explícito para mayor control. Dentro de las llaves también es posible especificar detalles adicionales sobre el formato de salida, como la cantidad de decimales o el uso de separadores de miles.

```python
# Formateo de cadenas con el método format()
host = "192.168.1.10"
puerto = 443

print("Host: {} - Puerto: {}".format(host, puerto))
# Host: 192.168.1.10 - Puerto: 443

print("Puerto: {1} - Host: {0}".format(host, puerto))
# Puerto: 443 - Host: 192.168.1.10
```

Un caso de uso particularmente frecuente del método `format()` es la inserción de separadores de miles al mostrar números grandes, como por ejemplo la cantidad total de combinaciones evaluadas durante un ataque de fuerza bruta:

```python
resultado = 35876543

print("{:,}".format(resultado))
# 35,876,543
```

En el caso de necesitar que el separador de miles se represente con un punto en lugar de una coma, como es habitual en el formato numérico de varios países de habla hispana, puede recurrirse al método `replace()` sobre la cadena ya formateada, sustituyendo la coma por el punto:

```python
resultado = 35876543

print("{:,}".format(resultado).replace(",", "."))
# 35.876.543
```

### F-Strings (Literal String Interpolation)

Disponibles desde Python 3.6, los *f-strings* constituyen la forma más concisa, legible y, en la actualidad, recomendada de incrustar expresiones dentro de literales de cadena. Se construyen anteponiendo la letra `f` justo antes de la comilla de apertura de la cadena, y permiten insertar variables o expresiones completas directamente dentro de llaves `{}`, sin necesidad de invocar métodos adicionales ni de mantener un orden separado entre la cadena y los valores a insertar.

```python
# Formateo de cadenas mediante f-strings
host = "192.168.1.10"
puerto = 443
tiempo_respuesta = 0.348

print(f"Host: {host} - Puerto: {puerto} - Tiempo: {tiempo_respuesta} seg")
# Host: 192.168.1.10 - Puerto: 443 - Tiempo: 0.348 seg

# Los f-strings también admiten expresiones evaluadas directamente dentro de las llaves
puertos_detectados = [22, 80, 443]
print(f"Cantidad de puertos abiertos: {len(puertos_detectados)}")
# Cantidad de puertos abiertos: 3
```

Gracias a su legibilidad y a la posibilidad de evaluar expresiones de forma directa, los f-strings se han convertido en el estándar de facto para el formateo de cadenas en proyectos modernos de Python, incluyendo la gran mayoría de scripts y herramientas de ciberseguridad, donde resulta habitual construir mensajes de log, reportes o salidas de consola combinando texto fijo con valores obtenidos dinámicamente durante la ejecución del programa.