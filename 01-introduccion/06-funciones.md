# Funciones y Ámbito de las Variables en Python

## Funciones

Las funciones son bloques de código reutilizables, diseñados para realizar una tarea específica y bien delimitada. Su uso constituye uno de los pilares fundamentales de la programación estructurada, ya que permiten dividir un programa complejo en piezas más pequeñas, comprensibles e independientes, evitando la repetición de código y facilitando tanto su mantenimiento como su prueba.

En Python, una función se define utilizando la palabra clave `def`, seguida de un nombre descriptivo, un par de paréntesis que pueden contener parámetros, y dos puntos que dan inicio al bloque de código indentado correspondiente al cuerpo de la función.

```python
def escanear_puerto(host, puerto):
    """Simula la verificación del estado de un puerto en un host determinado."""
    print(f"Verificando {host}:{puerto}...")
```

### Parámetros y Argumentos

Los parámetros son, en esencia, "variables de entrada" definidas en la firma de la función, cuyo valor concreto puede cambiar cada vez que la función es invocada. Esta característica es la que otorga a las funciones su versatilidad: una misma función puede operar sobre datos distintos en cada llamada, produciendo resultados acordes a los valores recibidos, sin necesidad de duplicar su lógica interna. Cabe aclarar que, en sentido estricto, se denomina _parámetro_ a la variable definida en la función, y _argumento_ al valor concreto que se proporciona al invocarla, aunque en la práctica ambos términos suelen utilizarse de forma intercambiable.

### La Sentencia `return`

Las funciones pueden devolver un valor al punto del programa desde el cual fueron invocadas mediante la palabra clave `return`. Esto permite que una función no solo ejecute una acción (como imprimir un mensaje en pantalla), sino que también procese datos de entrada y entregue un resultado calculado, el cual puede ser almacenado en una variable, utilizado en una expresión, o incluso pasado como argumento a otra función. Una función que no incluye una sentencia `return` explícita devuelve automáticamente el valor especial `None`.

```python
def es_puerto_critico(puerto):
    """Devuelve True si el puerto pertenece a la lista de puertos críticos conocidos."""
    puertos_criticos = [21, 23, 445, 3389]
    return puerto in puertos_criticos

resultado = es_puerto_critico(445)
print(resultado)   # True
```

## Tipos de Parámetros en Funciones

Python ofrece distintas formas de definir y proporcionar parámetros a una función, lo cual otorga una gran flexibilidad a la hora de diseñar su interfaz. Comprender estas variantes resulta esencial para escribir funciones claras y para poder utilizar correctamente las funciones provistas por bibliotecas de terceros, muchas de las cuales combinan varios de estos enfoques.

### Parámetros Posicionales

Los parámetros posicionales son la forma más básica de pasar argumentos a una función: los valores se asignan a los parámetros siguiendo estrictamente el orden en el que estos fueron definidos. Es responsabilidad de quien invoca la función respetar dicho orden, ya que un cambio en la posición de los argumentos altera por completo el resultado.

```python
def conectar(host, puerto, protocolo):
    print(f"Conectando a {host} en el puerto {puerto} usando {protocolo}")

# Los argumentos se asignan en el mismo orden en que fueron definidos los parámetros
conectar("192.168.1.10", 443, "https")
```

### Parámetros por Clave (_Keyword Arguments_)

Los parámetros por clave permiten especificar explícitamente a qué parámetro corresponde cada valor, indicando su nombre junto con el valor en el momento de la llamada. Esta forma de invocación tiene la ventaja de que el orden de los argumentos deja de ser relevante, ya que la asignación se realiza por nombre y no por posición, lo cual mejora considerablemente la legibilidad cuando una función admite varios parámetros.

```python
def conectar(host, puerto, protocolo):
    print(f"Conectando a {host} en el puerto {puerto} usando {protocolo}")

# El orden de los argumentos ya no importa, porque se especifican por nombre
conectar(protocolo="https", host="192.168.1.10", puerto=443)
```

Es posible, además, combinar argumentos posicionales y argumentos por clave dentro de una misma llamada, siempre y cuando los argumentos posicionales se especifiquen primero:

```python
# Combinación de argumento posicional y argumentos por clave
conectar("192.168.1.10", puerto=443, protocolo="https")
```

### Valores por Defecto

Asociado al uso de parámetros por clave, Python permite definir valores por defecto para uno o más parámetros de una función. Si al invocar la función no se proporciona un valor para dicho parámetro, se utilizará automáticamente el valor definido por defecto, lo que resulta útil para definir comportamientos habituales sin obligar a especificar todos los argumentos en cada llamada.

```python
def conectar(host, puerto=443, protocolo="https"):
    print(f"Conectando a {host} en el puerto {puerto} usando {protocolo}")

conectar("192.168.1.10")                       # usa puerto=443 y protocolo="https" por defecto
conectar("192.168.1.10", puerto=22, protocolo="ssh")  # sobrescribe ambos valores por defecto
```

### `*args`: Argumentos Posicionales Variables

En ocasiones, no se conoce de antemano cuántos argumentos posicionales recibirá una función. Para estos casos, Python ofrece la sintaxis `*args`, que permite a una función aceptar una cantidad arbitraria de argumentos posicionales, los cuales quedan agrupados internamente en una tupla. El nombre `args` es solo una convención; lo que define este comportamiento es el asterisco que lo precede.

```python
def escanear_puertos(host, *args):
    """Permite pasar una cantidad arbitraria de puertos a escanear."""
    print(f"Escaneando host {host} en los siguientes puertos:")
    for puerto in args:
        print(f"  -> Puerto {puerto}")

# La función admite tanto 2 como 5 puertos, o cualquier otra cantidad
escanear_puertos("192.168.1.10", 22, 80)
escanear_puertos("192.168.1.10", 21, 22, 80, 443, 3389)
```

Esta sintaxis resulta especialmente útil en herramientas de ciberseguridad donde la cantidad de objetivos, puertos o parámetros a evaluar puede variar de una ejecución a otra, evitando tener que definir de antemano un número fijo de argumentos o recurrir a una lista como único parámetro.

### `**kwargs`: Argumentos por Clave Variables

De forma análoga a `*args`, Python ofrece la sintaxis `**kwargs`, que permite a una función aceptar una cantidad arbitraria de argumentos por clave, los cuales quedan agrupados internamente en un diccionario, donde cada clave corresponde al nombre del argumento y cada valor al dato proporcionado. Al igual que con `args`, el nombre `kwargs` es una convención ampliamente adoptada, mientras que el comportamiento real lo determina el doble asterisco.

```python
def registrar_hallazgo(host, **kwargs):
    """Permite registrar un hallazgo con una cantidad variable de atributos adicionales."""
    print(f"Hallazgo registrado en {host}:")
    for clave, valor in kwargs.items():
        print(f"  -> {clave}: {valor}")

registrar_hallazgo(
    "192.168.1.10",
    puerto=22,
    servicio="ssh",
    version="OpenSSH 7.2",
    severidad="alta",
)
```

Es posible, además, combinar `*args` y `**kwargs` dentro de una misma función, lo cual es especialmente común en herramientas que envuelven o extienden el comportamiento de otras funciones, ya que permite reenviar cualquier combinación de argumentos sin necesidad de conocerlos de antemano:

```python
def ejecutar_modulo(nombre_modulo, *args, **kwargs):
    print(f"Ejecutando módulo: {nombre_modulo}")
    print(f"Argumentos posicionales: {args}")
    print(f"Argumentos por clave: {kwargs}")

ejecutar_modulo("port_scanner", "192.168.1.10", 22, 80, timeout=5, verbose=True)
```

## Ámbito de las Variables (_Scope_)

El ámbito, o _scope_, de una variable se refiere a la región del programa dentro de la cual dicha variable es visible y, por lo tanto, accesible. Comprender el ámbito de las variables resulta indispensable para evitar errores sutiles relacionados con el uso de nombres que, aunque puedan parecer idénticos, en realidad hacen referencia a variables completamente distintas dentro del programa. En Python existen principalmente dos tipos de ámbito: el ámbito local y el ámbito global.

### Ámbito Local

Las variables definidas dentro del cuerpo de una función poseen un ámbito local: solo pueden ser accedidas y modificadas desde dentro de esa misma función, y dejan de existir una vez que la función finaliza su ejecución. Esto implica que dos funciones distintas pueden utilizar variables con el mismo nombre sin que exista ningún tipo de conflicto entre ellas, ya que cada una mantiene su propio espacio de nombres independiente.

```python
def analizar_host(host):
    estado = "activo"   # variable local, solo existe dentro de esta función
    print(f"{host}: {estado}")

analizar_host("192.168.1.10")

# Intentar acceder a 'estado' fuera de la función produciría un error,
# ya que esa variable no existe en este ámbito
# print(estado)  # NameError: name 'estado' is not defined
```

### Ámbito Global

Las variables definidas fuera de cualquier función, directamente en el cuerpo principal del script, poseen un ámbito global: pueden ser leídas desde cualquier parte del programa, incluyendo desde dentro de funciones. Sin embargo, por defecto, Python no permite modificar el valor de una variable global desde dentro de una función simplemente reasignándola; al hacerlo, se estaría creando una nueva variable local con el mismo nombre, que coexiste con la variable global sin afectarla.

```python
contador_hosts_activos = 0   # variable global

def registrar_host_activo():
    # Esto NO modifica la variable global; crea una variable local nueva
    contador_hosts_activos = contador_hosts_activos + 1   # UnboundLocalError
```

Para modificar efectivamente una variable global desde dentro de una función, es necesario declararla explícitamente con la palabra clave `global` al comienzo de la función. Esto le indica a Python que, dentro de ese bloque, cualquier referencia a esa variable debe apuntar a la variable global, y no crear una nueva variable local.

```python
contador_hosts_activos = 0   # variable global

def registrar_host_activo():
    global contador_hosts_activos
    contador_hosts_activos += 1   # ahora sí modifica la variable global

registrar_host_activo()
registrar_host_activo()
registrar_host_activo()

print(f"Hosts activos registrados: {contador_hosts_activos}")   # 3
```

Si bien el uso de `global` resuelve el problema técnico, en general se considera una buena práctica de diseño limitar al mínimo posible la dependencia de variables globales mutables dentro de funciones, ya que su uso extendido tiende a dificultar el seguimiento del flujo de datos del programa y puede generar efectos secundarios difíciles de rastrear, especialmente en scripts de mayor tamaño. Una alternativa habitualmente preferida es que la función reciba el dato que necesita como parámetro y devuelva el resultado mediante `return`, dejando que sea el código que invoca a la función quien decida si actualiza o no una variable externa.
