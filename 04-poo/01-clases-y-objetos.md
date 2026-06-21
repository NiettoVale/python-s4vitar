# Programación Orientada a Objetos en Python: Clases, Decoradores y Métodos Especiales

## Introducción al Paradigma de la Programación Orientada a Objetos

La Programación Orientada a Objetos (POO) es un paradigma de programación que organiza el código en torno a dos conceptos centrales: los **objetos** y las **clases**. A diferencia de un enfoque puramente procedural, en el que un programa se concibe como una secuencia de funciones que operan sobre datos sueltos, la POO propone agrupar los datos y el comportamiento que opera sobre esos datos dentro de una misma unidad conceptual. Esta forma de organizar el código no es arbitraria: refleja, de manera bastante directa, la forma en que los seres humanos solemos razonar sobre las entidades del mundo real, pensando en términos de "cosas" que tienen ciertas características (atributos) y que pueden realizar ciertas acciones (comportamientos), en lugar de pensar en listas de instrucciones desconectadas entre sí.

Para quien trabaja en ciberseguridad, este paradigma resulta especialmente natural, porque gran parte de los conceptos con los que se trabaja a diario —un host, un puerto, un hallazgo de auditoría, una sesión de explotación, un payload— tienen exactamente esta forma: poseen un conjunto de atributos que los describen (una dirección IP, un estado, una severidad) y un conjunto de acciones que se pueden realizar sobre ellos o con ellos (escanear, explotar, reportar). Modelar estas entidades como clases, en lugar de como diccionarios sueltos y funciones independientes, permite construir herramientas más organizadas, más fáciles de extender, y más cercanas a la forma en que conceptualmente pensamos el problema que estamos resolviendo.

## Clases

Las clases constituyen el elemento fundacional de la Programación Orientada a Objetos. Una clase actúa como una plantilla o un molde a partir del cual se crean objetos concretos, y es responsable de definir tanto los atributos (los datos que cada objeto tendrá) como los comportamientos (las acciones que cada objeto podrá ejecutar) que tendrán todos los objetos derivados de ella. En Python, una clase se define utilizando la palabra clave `class`, seguida del nombre de la clase (por convención, escrito en `CamelCase`, como se mencionó en notas anteriores sobre PEP 8) y dos puntos, dando inicio a un bloque de código indentado que constituye el cuerpo de la clase.

```python
class Host:
    """Representa un host descubierto durante un proceso de reconocimiento."""

    def __init__(self, direccion_ip, sistema_operativo="desconocido"):
        # __init__ es el constructor: se ejecuta automáticamente al crear cada objeto
        self.direccion_ip = direccion_ip
        self.sistema_operativo = sistema_operativo
        self.puertos_abiertos = []
        self.activo = True
```

El método especial `__init__`, conocido como **constructor**, es invocado automáticamente por Python cada vez que se crea un nuevo objeto a partir de la clase, y es el lugar donde habitualmente se inicializan los atributos propios de cada objeto. El primer parámetro de `__init__`, así como el de prácticamente cualquier método definido dentro de una clase, es `self`, una referencia a la instancia concreta sobre la cual se está operando; este parámetro se recibe automáticamente y no se proporciona explícitamente al invocar el método desde fuera de la clase, pero sí debe declararse explícitamente en la definición del método.

## Instancias de Clase y Objetos

Un objeto es una instancia concreta de una clase: el resultado tangible de aplicar la plantilla definida por la clase para crear una entidad particular, con su propio espacio de memoria y su propio conjunto de valores para los atributos definidos por dicha clase. Cada vez que se invoca una clase como si fuera una función (es decir, escribiendo el nombre de la clase seguido de paréntesis), Python crea una nueva instancia independiente, ejecuta su método `__init__` para inicializarla, y devuelve esa instancia recién creada.

```python
host_uno = Host("192.168.1.10", sistema_operativo="Linux")
host_dos = Host("192.168.1.11", sistema_operativo="Windows")

# Cada objeto tiene su propio estado independiente, aunque ambos provienen de la misma clase
print(host_uno.direccion_ip, host_uno.sistema_operativo)   # 192.168.1.10 Linux
print(host_dos.direccion_ip, host_dos.sistema_operativo)   # 192.168.1.11 Windows

host_uno.puertos_abiertos.append(22)
print(host_uno.puertos_abiertos)   # [22]
print(host_dos.puertos_abiertos)   # []   <- no se vio afectado, son objetos independientes
```

Este ejemplo ilustra un concepto central de la POO conocido como **encapsulamiento**: cada objeto agrupa, dentro de una misma entidad discreta, tanto sus datos (atributos) como las funciones capaces de operar sobre esos datos (métodos), de modo que el estado de un objeto queda lógicamente contenido dentro de sí mismo, en lugar de dispersarse en variables sueltas y funciones externas que deban coordinarse manualmente para mantener la coherencia de los datos.

## Métodos de Clase (Métodos de Instancia)

Los métodos son funciones definidas dentro del cuerpo de una clase, y constituyen el mecanismo principal mediante el cual los objetos realizan acciones, modifican su propio estado, o interactúan con otros objetos. Es importante remarcar una distinción terminológica que suele generar confusión: lo que en estas notas iniciales se denomina genéricamente "métodos de clase" en un sentido amplio, en realidad corresponde, técnicamente, a **métodos de instancia**, ya que se invocan sobre una instancia particular de la clase (y reciben automáticamente esa instancia como primer argumento, `self`). Esto se distingue de los **métodos de clase** en sentido estricto, una categoría especial que se abordará en profundidad más adelante, asociada al decorador `@classmethod`.

```python
class Host:
    def __init__(self, direccion_ip, sistema_operativo="desconocido"):
        self.direccion_ip = direccion_ip
        self.sistema_operativo = sistema_operativo
        self.puertos_abiertos = []
        self.activo = True

    def agregar_puerto(self, puerto):
        """Método de instancia: opera sobre el estado particular de ESTE objeto."""
        if puerto not in self.puertos_abiertos:
            self.puertos_abiertos.append(puerto)

    def resumen(self):
        """Otro método de instancia, que lee el estado actual del objeto para generar un texto."""
        estado = "activo" if self.activo else "inactivo"
        return f"{self.direccion_ip} ({estado}) - puertos: {self.puertos_abiertos}"

host = Host("192.168.1.10")
host.agregar_puerto(22)
host.agregar_puerto(443)
print(host.resumen())   # 192.168.1.10 (activo) - puertos: [22, 443]
```

## Decoradores en Python

Los decoradores son, probablemente, una de las herramientas más poderosas y a la vez más mal comprendidas del lenguaje Python, y merecen una explicación detallada partiendo desde sus fundamentos, antes de abordar los decoradores específicos del paradigma orientado a objetos como `@classmethod` y `@staticmethod`.

### Funciones como Objetos de Primera Clase

Para comprender realmente cómo funciona un decorador, es necesario partir de un principio fundamental del lenguaje: en Python, las funciones son **objetos de primera clase** (_first-class objects_). Esto significa que una función puede tratarse exactamente igual que cualquier otro valor del lenguaje: puede asignarse a una variable, puede pasarse como argumento a otra función, y puede ser devuelta como resultado desde otra función, tal como ya se observó previamente al estudiar funciones lambda combinadas con `sorted()`, `map()` y `filter()`.

```python
def saludar():
    return "Hola, analista"

# La función puede asignarse a una variable, sin invocarla (nótese: sin paréntesis)
referencia_funcion = saludar
print(referencia_funcion())   # "Hola, analista"   <- se invoca a través de la nueva variable
```

### El Concepto de "Envoltorio" (_Wrapper_)

Un decorador es, en esencia, una función que recibe otra función como argumento, y devuelve una **nueva función** que envuelve el comportamiento de la función original, añadiendo lógica adicional antes y/o después de su ejecución, sin necesidad de modificar el código fuente original de la función decorada. Para construir un decorador "a mano", sin todavía utilizar la sintaxis especial `@`, se puede definir una función que recibe una función como parámetro, define internamente una nueva función ("la envoltura" o _wrapper_) que llama a la función original en algún punto de su lógica, y devuelve esa envoltura.

```python
def registrar_ejecucion(funcion_original):
    """Un decorador básico: registra cuándo se ejecuta la función que envuelve."""

    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando '{funcion_original.__name__}'...")
        resultado = funcion_original(*args, **kwargs)   # se invoca la función original aquí
        print(f"[LOG] '{funcion_original.__name__}' finalizó")
        return resultado

    return envoltura

def escanear_puerto(host, puerto):
    print(f"Escaneando {host}:{puerto}")
    return True

# Decorar "a mano", sin la sintaxis @ todavía
escanear_puerto = registrar_ejecucion(escanear_puerto)
escanear_puerto("192.168.1.10", 443)
```

```
[LOG] Ejecutando 'escanear_puerto'...
Escaneando 192.168.1.10:443
[LOG] 'escanear_puerto' finalizó
```

Obsérvese que la función `envoltura` utiliza `*args` y `**kwargs` (vistos en notas anteriores) precisamente para poder aceptar y reenviar cualquier combinación de argumentos hacia la función original, sin necesidad de conocer de antemano su firma exacta, lo cual permite que un mismo decorador pueda aplicarse a funciones con parámetros completamente distintos entre sí.

### La Sintaxis `@`: Azúcar Sintáctico

La línea `escanear_puerto = registrar_ejecucion(escanear_puerto)` del ejemplo anterior es exactamente lo que la sintaxis especial `@nombre_decorador`, colocada justo encima de la definición de una función, realiza de forma automática e implícita. Esta sintaxis es lo que se conoce como "azúcar sintáctico": una forma más legible y conveniente de expresar algo que, por debajo, sigue siendo el mismo mecanismo de reasignación de funciones recién descrito.

```python
def registrar_ejecucion(funcion_original):
    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando '{funcion_original.__name__}'...")
        resultado = funcion_original(*args, **kwargs)
        print(f"[LOG] '{funcion_original.__name__}' finalizó")
        return resultado
    return envoltura

@registrar_ejecucion   # esto es exactamente equivalente a: escanear_puerto = registrar_ejecucion(escanear_puerto)
def escanear_puerto(host, puerto):
    print(f"Escaneando {host}:{puerto}")
    return True

escanear_puerto("192.168.1.10", 443)   # se invoca como si fuera la función original, pero está decorada
```

### Preservando los Metadatos de la Función Original con `functools.wraps`

Un detalle técnico importante, frecuentemente pasado por alto, es que al envolver una función dentro de otra, se pierde el acceso a los metadatos originales de la función decorada, como su nombre (`__name__`) o su _docstring_, ya que lo que queda expuesto públicamente es, en realidad, la función `envoltura`. Para evitar este efecto secundario indeseado, la biblioteca estándar ofrece el decorador `functools.wraps`, que se aplica sobre la propia función `envoltura` y se encarga de copiar automáticamente los metadatos relevantes desde la función original.

```python
import functools

def registrar_ejecucion(funcion_original):
    @functools.wraps(funcion_original)   # preserva __name__, __doc__, etc. de la función original
    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando '{funcion_original.__name__}'...")
        return funcion_original(*args, **kwargs)
    return envoltura

@registrar_ejecucion
def escanear_puerto(host, puerto):
    """Simula el escaneo de un puerto específico."""
    return True

print(escanear_puerto.__name__)   # "escanear_puerto"   <- sin @wraps, esto habría sido "envoltura"
print(escanear_puerto.__doc__)    # "Simula el escaneo de un puerto específico."
```

Este detalle, aunque pequeño, se considera una buena práctica estándar de la comunidad Python al escribir cualquier decorador, ya que su ausencia puede generar confusión al inspeccionar o depurar código decorado, e interfiere con herramientas que dependen de estos metadatos, como ciertos sistemas de documentación automática.

### Decoradores con Parámetros Propios

En ocasiones, se necesita que el propio decorador admita parámetros de configuración, como por ejemplo, la cantidad de reintentos a realizar antes de considerar fallida una operación. Esto requiere un nivel adicional de anidamiento: una función "exterior" que recibe los parámetros del decorador y devuelve el decorador propiamente dicho, el cual a su vez recibe la función a decorar y devuelve la envoltura final.

```python
import functools
import time

def reintentar(intentos_maximos=3, espera_segundos=1):
    """Decorador parametrizable: reintenta una función ante una excepción."""

    def decorador(funcion_original):
        @functools.wraps(funcion_original)
        def envoltura(*args, **kwargs):
            for intento in range(1, intentos_maximos + 1):
                try:
                    return funcion_original(*args, **kwargs)
                except ConnectionError as error:
                    print(f"Intento {intento}/{intentos_maximos} falló: {error}")
                    if intento == intentos_maximos:
                        raise
                    time.sleep(espera_segundos)
        return envoltura

    return decorador

@reintentar(intentos_maximos=3, espera_segundos=0.5)
def conectar_a_host(host):
    raise ConnectionError(f"No se pudo conectar con {host}")

try:
    conectar_a_host("192.168.1.250")
except ConnectionError:
    print("Se agotaron todos los reintentos")
```

### Casos de Uso Habituales de los Decoradores en Ciberseguridad

Más allá del ejemplo de registro de ejecución (_logging_) ya desarrollado, los decoradores tienen aplicaciones extremadamente prácticas en el desarrollo de herramientas de ciberseguridad. Un caso frecuente es medir el tiempo de ejecución de una función, útil para perfilar el rendimiento de un escaneo:

```python
import functools
import time

def medir_tiempo(funcion_original):
    @functools.wraps(funcion_original)
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = funcion_original(*args, **kwargs)
        duracion = time.perf_counter() - inicio
        print(f"'{funcion_original.__name__}' tardó {duracion:.4f} segundos")
        return resultado
    return envoltura

@medir_tiempo
def escanear_red(rango_cidr):
    time.sleep(0.2)   # simula el tiempo que tomaría un escaneo real
    return ["192.168.1.10", "192.168.1.11"]

hosts_encontrados = escanear_red("192.168.1.0/24")
```

Otro caso de uso extremadamente relevante es la verificación de permisos antes de ejecutar una acción potencialmente sensible, un patrón habitual en herramientas que distinguen entre distintos niveles de privilegio de usuario dentro de la propia herramienta:

```python
import functools

def requiere_permiso(nivel_requerido):
    """Decorador parametrizable que verifica el nivel de permiso del usuario actual."""

    def decorador(funcion_original):
        @functools.wraps(funcion_original)
        def envoltura(usuario_actual, *args, **kwargs):
            if usuario_actual.get("nivel", 0) < nivel_requerido:
                raise PermissionError(
                    f"Se requiere nivel {nivel_requerido}, el usuario tiene nivel {usuario_actual.get('nivel', 0)}"
                )
            return funcion_original(usuario_actual, *args, **kwargs)
        return envoltura

    return decorador

@requiere_permiso(nivel_requerido=3)
def eliminar_hallazgo(usuario_actual, id_hallazgo):
    print(f"Hallazgo {id_hallazgo} eliminado por {usuario_actual['nombre']}")

analista_junior = {"nombre": "analista_jr", "nivel": 1}
analista_senior = {"nombre": "analista_sr", "nivel": 5}

try:
    eliminar_hallazgo(analista_junior, "H-001")
except PermissionError as error:
    print(f"Acceso denegado: {error}")

eliminar_hallazgo(analista_senior, "H-001")   # este sí tiene permiso suficiente
```

Finalmente, un caso de uso muy citado es la memorización de resultados (_memoization_ o _caching_), que evita recalcular o reconsultar un resultado costoso si ya se obtuvo previamente con los mismos argumentos. La biblioteca estándar ofrece directamente `functools.lru_cache` para este propósito, pero comprender su construcción manual ayuda a entender el principio subyacente:

```python
import functools

def con_cache(funcion_original):
    """Decorador simple de memorización: guarda resultados previos según los argumentos recibidos."""
    cache = {}

    @functools.wraps(funcion_original)
    def envoltura(*args):
        if args in cache:
            print(f"[CACHE] Resultado reutilizado para {args}")
            return cache[args]
        resultado = funcion_original(*args)
        cache[args] = resultado
        return resultado
    return envoltura

@con_cache
def resolver_dns(host):
    print(f"Resolviendo DNS para {host}... (operación costosa simulada)")
    return f"IP simulada de {host}"

resolver_dns("ejemplo.com")   # se ejecuta de verdad
resolver_dns("ejemplo.com")   # se reutiliza desde el caché, sin volver a "resolver"
```

## Métodos de Clase y Métodos Estáticos

Habiendo comprendido en profundidad qué es y cómo funciona un decorador, es momento de abordar dos decoradores específicos del contexto de la Programación Orientada a Objetos: `@classmethod` y `@staticmethod`. Ambos modifican la forma en que un método definido dentro de una clase recibe (o no recibe) una referencia implícita a la instancia o a la propia clase, y ambos resultan extremadamente útiles para enriquecer el diseño de las clases que se construyen en un proyecto.

### Métodos de Clase: `@classmethod`

Un método de clase es un método que está ligado a la clase en su totalidad, y no a una instancia particular de dicha clase. Esto significa que puede invocarse directamente sobre la clase misma, sin necesidad de haber creado previamente un objeto. Se definen utilizando el decorador `@classmethod`, y su primer parámetro, por convención llamado `cls` (en lugar de `self`), es una referencia automática a la propia clase, de forma análoga a como `self` es una referencia automática a la instancia en un método de instancia regular.

El uso más característico de los métodos de clase es la implementación de **métodos factory** (métodos de fábrica): constructores alternativos que permiten crear instancias de la clase a partir de distintas fuentes de datos o con distinta lógica de inicialización, sin sobrecargar el único constructor `__init__` con múltiples formas incompatibles de recibir argumentos.

```python
class Host:
    def __init__(self, direccion_ip, sistema_operativo="desconocido"):
        self.direccion_ip = direccion_ip
        self.sistema_operativo = sistema_operativo
        self.puertos_abiertos = []

    @classmethod
    def desde_linea_nmap(cls, linea_csv):
        """Método factory: construye un Host a partir de una línea de salida CSV de nmap."""
        # Ejemplo de línea: "192.168.1.10,Linux,22;80;443"
        ip, so, puertos_texto = linea_csv.split(",")
        nuevo_host = cls(ip, sistema_operativo=so)   # 'cls' actúa como el nombre de la clase: Host(...)
        nuevo_host.puertos_abiertos = [int(p) for p in puertos_texto.split(";")]
        return nuevo_host

    def resumen(self):
        return f"{self.direccion_ip} ({self.sistema_operativo}) - {self.puertos_abiertos}"

# Constructor estándar
host_manual = Host("192.168.1.20")

# Constructor alternativo, vía método de clase, a partir de un formato de datos distinto
host_desde_nmap = Host.desde_linea_nmap("192.168.1.10,Linux,22;80;443")
print(host_desde_nmap.resumen())   # 192.168.1.10 (Linux) - [22, 80, 443]
```

Otra aplicación relevante de los métodos de clase consiste en modificar **atributos de clase**, es decir, atributos definidos directamente en el cuerpo de la clase (fuera de `__init__`) y compartidos por todas las instancias de dicha clase, en lugar de pertenecer individualmente a cada objeto. Mientras que un método de instancia, a través de `self`, normalmente solo afecta al estado del objeto particular sobre el que se invoca, un método de clase, a través de `cls`, puede modificar ese estado compartido, afectando potencialmente a todas las instancias existentes y futuras.

```python
class Host:
    contador_hosts_creados = 0   # atributo de clase: compartido por TODAS las instancias

    def __init__(self, direccion_ip):
        self.direccion_ip = direccion_ip
        Host.contador_hosts_creados += 1   # se incrementa el contador compartido en cada creación

    @classmethod
    def total_hosts_creados(cls):
        return cls.contador_hosts_creados

Host("192.168.1.10")
Host("192.168.1.11")
Host("192.168.1.12")

print(Host.total_hosts_creados())   # 3   <- el método de clase se invoca sobre la clase, no sobre un objeto
```

### Métodos Estáticos: `@staticmethod`

Un método estático, definido mediante el decorador `@staticmethod`, no recibe ninguna referencia implícita, ni a la instancia (`self`) ni a la clase (`cls`). En la práctica, un método estático se comporta exactamente como una función regular e independiente, con la única diferencia de que, por razones de organización y cohesión del código, se define dentro del cuerpo de la clase porque su funcionalidad está temáticamente relacionada con ella, aunque no necesite acceder a ninguno de sus atributos ni de sus métodos.

```python
class Host:
    def __init__(self, direccion_ip):
        if not Host.es_ip_valida(direccion_ip):
            raise ValueError(f"'{direccion_ip}' no es una dirección IP válida")
        self.direccion_ip = direccion_ip

    @staticmethod
    def es_ip_valida(direccion_ip):
        """Método estático: una validación de formato que no depende de ningún objeto Host concreto."""
        partes = direccion_ip.split(".")
        if len(partes) != 4:
            return False
        return all(parte.isdigit() and 0 <= int(parte) <= 255 for parte in partes)

# El método estático puede invocarse sobre la clase, sin necesidad de una instancia
print(Host.es_ip_valida("192.168.1.10"))    # True
print(Host.es_ip_valida("999.999.1.1"))     # False

# También puede invocarse sobre una instancia ya creada, con idéntico resultado
host = Host("192.168.1.10")
print(host.es_ip_valida("10.0.0.1"))        # True
```

En este ejemplo, `es_ip_valida()` resulta conceptualmente apropiada dentro de la clase `Host`, ya que su propósito está directamente relacionado con la validación de direcciones IP, pero su lógica interna no necesita en absoluto acceder a ningún atributo particular de una instancia (`self`) ni del estado compartido de la clase (`cls`): simplemente opera sobre el argumento que recibe, exactamente igual que lo haría una función definida fuera de la clase. Definirla como método estático, en lugar de como una función suelta en el módulo, comunica claramente que esta validación pertenece, conceptualmente, al dominio de la clase `Host`, mejorando la organización y la cohesión del código.

### Comparación entre Método de Instancia, Método de Clase y Método Estático

Para sintetizar las diferencias entre los tres tipos de métodos que pueden definirse dentro de una clase en Python, conviene observarlos en conjunto dentro de un mismo ejemplo, prestando atención a qué referencia implícita recibe cada uno y sobre qué se invocan habitualmente.

```python
class Escaner:
    motor_version = "2.1.0"   # atributo de clase

    def __init__(self, objetivo):
        self.objetivo = objetivo   # atributo de instancia

    def ejecutar(self):
        # Método de instancia: recibe 'self', accede al estado particular de ESTE objeto
        print(f"Escaneando {self.objetivo} con el motor {self.motor_version}")

    @classmethod
    def info_motor(cls):
        # Método de clase: recibe 'cls', accede al estado compartido por TODAS las instancias
        return f"Motor de escaneo versión {cls.motor_version}"

    @staticmethod
    def es_objetivo_valido(objetivo):
        # Método estático: no recibe self ni cls, es una función independiente alojada en la clase
        return isinstance(objetivo, str) and len(objetivo) > 0

escaner = Escaner("192.168.1.10")
escaner.ejecutar()                       # método de instancia: requiere un objeto creado
print(Escaner.info_motor())              # método de clase: se invoca sobre la clase directamente
print(Escaner.es_objetivo_valido("192.168.1.10"))   # método estático: tampoco requiere una instancia
```

La elección entre uno u otro tipo de método depende, en definitiva, de qué información necesita ese fragmento de lógica para funcionar: si necesita el estado particular de un objeto concreto, corresponde un método de instancia; si necesita operar sobre la clase en su conjunto (típicamente para construir instancias de formas alternativas o gestionar estado compartido), corresponde un método de clase; y si no necesita ni lo uno ni lo otro, pero pertenece temáticamente a la clase por motivos de organización, corresponde un método estático.

## Buenas Prácticas

A la hora de diseñar una clase, conviene reflexionar explícitamente sobre el tipo de método más apropiado para cada funcionalidad, en lugar de definir todo como métodos de instancia por defecto: forzar al primer parámetro `self` en un método que en realidad no utiliza ningún atributo de la instancia es una señal habitual de que dicho método debería ser, en realidad, un método estático, lo cual comunica con mayor precisión su verdadera naturaleza a cualquier persona que lea el código posteriormente.

En cuanto a los decoradores personalizados, conviene aplicar siempre `functools.wraps` sobre la función de envoltura, salvo en casos excepcionales donde se desee deliberadamente ocultar los metadatos originales, ya que omitir este detalle dificulta la depuración y puede romper herramientas de documentación o introspección que dependen de `__name__` y `__doc__`. Asimismo, al construir decoradores parametrizables, conviene mantener presente la estructura de triple anidamiento (la función exterior que recibe los parámetros del decorador, la función decoradora propiamente dicha que recibe la función a decorar, y la función de envoltura final), ya que confundir estos niveles es una de las fuentes de error más comunes al escribir decoradores avanzados por primera vez.

Finalmente, respecto a los métodos de clase, conviene reservarlos principalmente para dos escenarios bien delimitados: la implementación de constructores alternativos (métodos factory), que mejoran considerablemente la legibilidad frente a sobrecargar un único `__init__` con lógica condicional compleja para distintos formatos de entrada; y la gestión deliberada de estado verdaderamente compartido entre todas las instancias de una clase, como contadores globales o configuraciones que deben afectar a la clase en su conjunto, evitando recurrir a atributos de clase mutables cuando, en realidad, el dato en cuestión debería pertenecer de forma individual a cada instancia.
