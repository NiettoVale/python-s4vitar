# Tipos de Datos Fundamentales en Python: Variables, Cadenas, Números y Listas

## Variables

En Python, una variable es esencialmente un nombre simbólico que se asocia a un dato almacenado en memoria. A diferencia de lenguajes como C o Java, Python no requiere que el programador declare explícitamente el tipo de dato que va a contener una variable, ya que el intérprete es capaz de inferirlo automáticamente a partir del valor que se le asigna en el momento de la creación. Esta característica forma parte del tipado dinámico mencionado anteriormente, y permite escribir código de forma más ágil, aunque traslada al programador la responsabilidad de tener presente, en todo momento, qué tipo de dato contiene cada variable.

```python
# Python infiere el tipo de dato automáticamente, sin declaraciones previas
objetivo = "192.168.1.10"   # cadena (str)
puerto = 443                 # entero (int)
ssl_activo = True            # booleano (bool)
```

## Cadenas (Strings)

Las cadenas, o *strings*, son secuencias de caracteres utilizadas para representar y manipular texto. En Python se definen delimitando el contenido entre comillas simples o dobles, y constituyen uno de los tipos de datos más utilizados en cualquier script, ya sea para construir mensajes, generar payloads, parsear salidas de herramientas o componer rutas de archivos y direcciones de red.

Una propiedad fundamental de las cadenas es que son **inmutables**: una vez creada una cadena, no es posible modificar uno de sus caracteres individuales accediendo a su posición. Cualquier operación que aparente "modificar" una cadena en realidad genera una nueva cadena en memoria, dejando la original intacta.

```python
ip = "192.168.1.10"

# Esto generaría un error, ya que las cadenas no permiten asignación por índice
# ip[0] = "X"   # TypeError: 'str' object does not support item assignment

# La forma correcta de "modificar" una cadena es crear una nueva
ip_modificada = "X" + ip[1:]
print(ip_modificada)   # X92.168.1.10
```

## Números

Python admite varios tipos numéricos, pero en esta etapa nos centraremos en los dos más utilizados en la práctica diaria de programación: los enteros y los flotantes.

Los **enteros** (*integers*, tipo `int`) representan números sin parte decimal, y se emplean habitualmente para contar elementos, representar puertos, índices o cantidades de intentos en un script. Los **flotantes** (*floats*, tipo `float`), por su parte, son números que incluyen una parte decimal, y resultan necesarios cuando se requiere precisión fraccionaria, como al calcular tiempos de respuesta, porcentajes o promedios.

```python
intentos_realizados = 3        # int: cantidad de intentos en un ataque de fuerza bruta
tiempo_respuesta = 0.348       # float: tiempo de respuesta de un host, en segundos
```

## Listas

### Introducción

Una lista en Python es una colección **ordenada** y **mutable** de elementos, capaz de almacenar datos de distintos tipos dentro de una misma estructura. A diferencia de las cadenas, las listas sí permiten modificar, añadir o eliminar elementos después de haber sido creadas, lo que las convierte en una de las estructuras de datos más versátiles y utilizadas del lenguaje. Su carácter ordenado implica que cada elemento ocupa una posición (índice) específica dentro de la colección, comenzando siempre desde el índice cero.

Las listas se definen utilizando corchetes `[ ]`, separando cada elemento mediante comas:

```python
# Una lista de puertos comúnmente escaneados durante un reconocimiento
puertos_comunes = [21, 22, 23, 80, 443, 445, 3389]

# Una lista puede combinar distintos tipos de datos en su interior
resultado_host = ["192.168.1.10", 22, "ssh", True]
```

### Características y Operaciones Básicas

Al ser estructuras mutables, las listas permiten agregar nuevos elementos mediante el método `append()`, eliminar elementos por su valor con `remove()`, o acceder y modificar un elemento puntual a través de su índice. También admiten operaciones de *slicing*, que permiten extraer subconjuntos de la lista original sin alterarla.

```python
# Lista de hosts activos detectados en una red durante un escaneo
hosts_activos = ["192.168.1.1", "192.168.1.10", "192.168.1.15"]

# Acceso por índice (el primer elemento es el índice 0)
primer_host = hosts_activos[0]      # "192.168.1.1"

# Agregar un nuevo host descubierto a la lista
hosts_activos.append("192.168.1.20")

# Eliminar un host que ya no está activo
hosts_activos.remove("192.168.1.1")

# Slicing: obtener los dos primeros elementos de la lista
primeros_dos = hosts_activos[0:2]

print(hosts_activos)
```

Una lista también puede contener otras listas en su interior, dando lugar a estructuras anidadas que resultan útiles para representar información más compleja, como los resultados de un escaneo en el que cada host tiene asociados varios puertos abiertos:

```python
# Lista de listas: cada sublista representa un host con sus puertos abiertos
escaneo = [
    ["192.168.1.10", [22, 80, 443]],
    ["192.168.1.15", [21, 23, 3389]],
]
```

### Recorrido de Listas con el Bucle `for`

Para trabajar de forma eficiente con listas, así como con cadenas y rangos de números, se emplea el bucle `for`, que permite iterar sobre cada elemento de una secuencia de manera ordenada, ejecutando un bloque de código para cada uno de ellos sin necesidad de gestionar manualmente índices ni condiciones de corte.

```python
# Recorrer una lista de puertos comunes e informar cuáles se consideran críticos
puertos_comunes = [21, 22, 23, 80, 443, 445, 3389]
puertos_criticos = [23, 445, 3389]

for puerto in puertos_comunes:
    if puerto in puertos_criticos:
        print(f"[!] Puerto {puerto} considerado de alto riesgo")
    else:
        print(f"[+] Puerto {puerto} registrado para análisis")
```

El bucle `for` también puede combinarse con la función `enumerate()` cuando, además del valor de cada elemento, se necesita conocer su posición dentro de la lista, lo cual resulta útil al generar reportes numerados de resultados:

```python
# Generar un listado numerado de hosts activos detectados en el escaneo
hosts_activos = ["192.168.1.10", "192.168.1.15", "192.168.1.20"]

for indice, host in enumerate(hosts_activos, start=1):
    print(f"{indice}. Host activo encontrado: {host}")
```

Este patrón de iteración sobre listas mediante `for` es, en la práctica, la base de una gran cantidad de scripts de ciberseguridad: desde el recorrido de diccionarios de contraseñas en ataques de fuerza bruta, hasta el procesamiento de listas de subdominios, direcciones IP o resultados obtenidos de herramientas como `nmap`.
