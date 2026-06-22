# Creación y Distribución de Paquetes en Python

## Introducción

Crear y distribuir un paquete Python es el paso que convierte un conjunto de módulos locales en software que cualquier persona puede instalar con un simple `pip3 install nombre_paquete`. Es el proceso que separa una herramienta que solo funciona en tu máquina de una biblioteca que la comunidad puede adoptar, extender y mejorar. En el contexto de la ciberseguridad, este conocimiento resulta valioso tanto para distribuir herramientas propias como para comprender en profundidad cómo funciona el ecosistema de paquetes que se usa a diario, incluyendo los vectores de ataque asociados a él (como el _typosquatting_ en PyPI o las dependencias maliciosas).

## Estructura de Directorios de un Paquete

La estructura de directorios es la primera decisión a tomar al crear un paquete. Una buena estructura organiza el código de forma que sea fácil de leer, probar, documentar e instalar. A continuación se muestra la estructura estándar y recomendada por la comunidad para un paquete Python moderno:

```
recon_tool/                          <- directorio raíz del proyecto (repositorio)
│
├── src/                             <- convenio "src layout": el código vive aquí
│   └── recon_tool/                  <- el paquete en sí (importable)
│       ├── __init__.py
│       ├── scanner.py
│       ├── dns_enum.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── network.py
│       │   └── validators.py
│       └── reporting/
│           ├── __init__.py
│           └── markdown_report.py
│
├── tests/                           <- tests unitarios e integración
│   ├── __init__.py
│   ├── test_scanner.py
│   └── test_validators.py
│
├── docs/                            <- documentación
│   └── index.md
│
├── pyproject.toml                   <- archivo principal de configuración (moderno, recomendado)
├── setup.cfg                        <- metadatos complementarios (en proyectos que usan setuptools)
├── MANIFEST.in                      <- archivos adicionales a incluir en la distribución
├── README.md                        <- descripción del proyecto (se muestra en PyPI)
├── LICENSE                          <- licencia del paquete
└── requirements.txt                 <- dependencias para desarrollo local
```

La separación entre el directorio raíz del proyecto (que contiene los archivos de configuración, tests y documentación) y el directorio del paquete en sí (dentro de `src/`) es una convención denominada _src layout_, cada vez más adoptada en la comunidad porque evita que Python importe accidentalmente el código fuente local en lugar del paquete instalado durante las pruebas, lo que puede ocultar errores de instalación.

## El Archivo `__init__.py` del Paquete

Como se vio en notas anteriores, el `__init__.py` transforma un directorio en un paquete Python. En el contexto de la distribución, este archivo cobra especial importancia porque suele ser el lugar donde se define la versión del paquete y se expone la interfaz pública que los usuarios utilizarán.

```python
# src/recon_tool/__init__.py
"""
recon_tool: framework modular de reconocimiento ofensivo.

Uso básico:
    from recon_tool import escanear_host, enumerar_subdominios
"""

# Versión del paquete: definida aquí y referenciada desde pyproject.toml
__version__ = "1.0.0"
__author__ = "NiettoVale"
__license__ = "MIT"

# Se exponen los nombres más importantes para un acceso cómodo desde la raíz del paquete
from recon_tool.scanner import escanear_host
from recon_tool.dns_enum import enumerar_subdominios
from recon_tool.reporting.markdown_report import generar_reporte

# Controla qué se exporta con "from recon_tool import *"
__all__ = ["escanear_host", "enumerar_subdominios", "generar_reporte", "__version__"]
```

## Archivos de Configuración

### `pyproject.toml`: El Estándar Moderno

El archivo `pyproject.toml` es el estándar moderno y recomendado para configurar un paquete Python, definido en los PEPs 517 y 518. Reemplaza progresivamente al histórico `setup.py` y unifica en un único archivo tanto la configuración del proceso de construcción del paquete (_build system_) como los metadatos del mismo. El formato TOML (_Tom's Obvious, Minimal Language_) es legible, estructurado y soportado nativamente por las herramientas modernas del ecosistema Python.

```toml
# pyproject.toml

[build-system]
# Define qué herramienta se usará para construir el paquete.
# setuptools es la opción más clásica y ampliamente soportada.
# Alternativas modernas: flit, hatch, poetry.
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
# Metadatos del paquete: lo que aparecerá en PyPI
name = "recon-tool"
version = "1.0.0"
description = "Framework modular de reconocimiento ofensivo para pruebas de penetración."
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.9"

# Dependencias que pip instalará automáticamente junto con el paquete
dependencies = [
    "requests>=2.28.0",
    "dnspython>=2.3.0",
    "colorama>=0.4.6",
]

# Clasificadores: ayudan a PyPI a categorizar el paquete
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Security",
]

# Palabras clave que facilitan encontrar el paquete en PyPI
keywords = ["security", "reconnaissance", "pentesting", "port-scanning"]

# Información de contacto y URLs relevantes del proyecto
[project.urls]
Homepage = "https://github.com/<usuario>/recon-tool"
Repository = "https://github.com/<usuario>/recon-tool"
"Bug Tracker" = "https://github.com/<usuario>/recon-tool/issues"

# Scripts de consola: comandos que quedan disponibles en el PATH tras la instalación
# Esto es lo que permite ejecutar "recon-tool --target 192.168.1.0/24" desde la terminal
[project.scripts]
recon-tool = "recon_tool.main:main"

# Dependencias adicionales solo necesarias para desarrollo y pruebas
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "isort>=5.0",
]

[tool.setuptools.packages.find]
# Indica a setuptools dónde buscar los paquetes a incluir en la distribución
where = ["src"]
```

La sección `[project.scripts]` merece atención especial: define los **entry points** del paquete, es decir, los comandos de línea de comandos que quedan instalados globalmente en el sistema cuando el paquete se instala con `pip`. En el ejemplo, instalar `recon-tool` hace que el comando `recon-tool` quede disponible en la terminal, llamando automáticamente a la función `main()` del módulo `recon_tool.main`.

```python
# src/recon_tool/main.py
"""Punto de entrada del paquete: se invoca con el comando 'recon-tool'."""

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="recon-tool: framework modular de reconocimiento ofensivo"
    )
    parser.add_argument("--target", required=True, help="IP, rango CIDR o dominio objetivo")
    parser.add_argument("--ports", nargs="+", type=int, help="Puertos específicos a escanear")
    parser.add_argument("--output", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    # Aquí iría la lógica de orquestación de los módulos del framework
    print(f"Iniciando reconocimiento sobre {args.target}...")


if __name__ == "__main__":
    main()
```

### El Histórico `setup.py`

Antes de `pyproject.toml`, el archivo central de configuración era `setup.py`, un script de Python que invocaba la función `setup()` del paquete `setuptools`. Aunque actualmente se considera **desaconsejado** para proyectos nuevos (precisamente porque mezcla configuración con código ejecutable, lo que puede generar problemas de seguridad y reproducibilidad), sigue encontrándose en la mayoría de los proyectos existentes, por lo que resulta importante conocerlo.

```python
# setup.py (forma histórica, desaconsejada para proyectos nuevos)
from setuptools import setup, find_packages

setup(
    name="recon-tool",
    version="1.0.0",
    description="Framework modular de reconocimiento ofensivo.",
    author="NiettoVale",
    author_email="niettovale@ejemplo.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.28.0",
        "dnspython>=2.3.0",
    ],
    entry_points={
        "console_scripts": [
            "recon-tool=recon_tool.main:main",
        ],
    },
)
```

### El Archivo `MANIFEST.in`

Por defecto, al construir la distribución del paquete, las herramientas de construcción solo incluyen los archivos Python del paquete. El archivo `MANIFEST.in` permite especificar qué archivos adicionales deben incluirse en la distribución de código fuente (_source distribution_), como el `README.md`, el archivo de licencia, los archivos de configuración, o cualquier recurso de datos que el paquete necesite en tiempo de ejecución.

```
# MANIFEST.in
include README.md
include LICENSE
include pyproject.toml
recursive-include docs *.md
recursive-include src/recon_tool/data *.json *.yaml
```

### El Archivo `README.md`

El `README.md` es el primer punto de contacto de cualquier desarrollador que encuentre el paquete en PyPI o en un repositorio. PyPI lo renderiza automáticamente como la página principal del paquete, por lo que debe ser claro, completo y bien estructurado. Una estructura típica incluye: descripción breve del proyecto, características principales, requisitos del sistema, instrucciones de instalación, ejemplos de uso básico, y referencias a la documentación completa.

```markdown
# recon-tool

Framework modular de reconocimiento ofensivo para pruebas de penetración autorizadas.

## Instalación

\```bash
pip install recon-tool
\```

## Uso rápido

\```bash
recon-tool --target 192.168.1.0/24 --output markdown
\```

\```python
from recon_tool import escanear_host

puertos_abiertos = escanear_host("192.168.1.10")
print(puertos_abiertos)
\```

## Licencia

MIT
```

## El Proceso de Construcción y Distribución

### Construcción del Paquete

El proceso de construcción genera los archivos que serán subidos a PyPI. Existen dos tipos de distribuciones: la **source distribution** (`.tar.gz`, contiene el código fuente y los archivos de configuración) y la **wheel** (`.whl`, es un formato binario precompilado que permite instalaciones más rápidas al no requerir un paso de construcción en el equipo del usuario). Ambos formatos deben generarse para una distribución completa.

La herramienta moderna recomendada para construir ambos es el paquete `build`, que debe instalarse primero:

```bash
# Instalar las herramientas necesarias para construir y distribuir
pip3 install build twine

# Desde el directorio raíz del proyecto (donde está pyproject.toml),
# construir la source distribution y la wheel simultáneamente
python3 -m build
```

Al ejecutar este comando, se crea un directorio `dist/` con dos archivos:

```
dist/
├── recon_tool-1.0.0.tar.gz          <- source distribution
└── recon_tool-1.0.0-py3-none-any.whl  <- wheel (distribución binaria)
```

### Verificación del Paquete Construido

Antes de subir el paquete a PyPI, conviene verificar que los archivos generados son correctos y que los metadatos están bien formados. La herramienta `twine check` analiza los archivos de distribución y reporta cualquier problema antes de que llegue al repositorio público.

```bash
twine check dist/*
```

### Publicación en TestPyPI

TestPyPI es una instancia de PyPI destinada exclusivamente a pruebas: permite subir paquetes y verificar que todo el proceso de distribución funciona correctamente (metadatos, descripción, instalación) sin afectar al repositorio público de producción. El flujo recomendado es siempre publicar primero en TestPyPI, verificar el resultado, y solo entonces publicar en el PyPI real.

```bash
# Subir los archivos de distribución a TestPyPI
twine upload --repository testpypi dist/*

# Instalar el paquete desde TestPyPI para verificar que la instalación funciona
pip3 install --index-url https://test.pypi.org/simple/ recon-tool
```

### Publicación en PyPI

Una vez verificado el paquete en TestPyPI, el proceso de publicación en el PyPI real es idéntico, omitiendo el argumento `--repository`:

```bash
# Subir a PyPI (producción)
twine upload dist/*
```

Twine solicitará las credenciales de la cuenta de PyPI. Para automatizar el proceso (como en un pipeline de CI/CD), es posible usar tokens de API de PyPI en lugar de usuario y contraseña, especificando el token como variable de entorno o en el archivo de configuración `~/.pypirc`.

```ini
# ~/.pypirc
[pypi]
username = __token__
password = pypi-AgAAAA...   <- token de API generado en la cuenta de PyPI
```

Una vez publicado, el paquete queda disponible para cualquier persona con:

```bash
pip3 install recon-tool
```

## Versionado Semántico

El versionado de un paquete sigue convencionalmente el estándar **SemVer** (_Semantic Versioning_), cuyo formato es `MAJOR.MINOR.PATCH`:

- **MAJOR**: se incrementa al introducir cambios incompatibles con versiones anteriores de la API pública (un cambio que puede romper código existente que usaba versiones anteriores del paquete).
- **MINOR**: se incrementa al agregar nueva funcionalidad de forma retrocompatible (nuevas funciones o parámetros opcionales que no rompen el código existente).
- **PATCH**: se incrementa al corregir errores de forma retrocompatible (bugfixes que no cambian la API).

```
1.0.0   <- primera versión estable de producción
1.0.1   <- corrección de un bug
1.1.0   <- nueva funcionalidad, sin romper compatibilidad
2.0.0   <- cambio incompatible (rompe la API anterior)
```

Las versiones de prelanzamiento se marcan con sufijos como `1.0.0a1` (alpha), `1.0.0b1` (beta), `1.0.0rc1` (release candidate). Nunca debe publicarse dos veces la misma versión en PyPI: una vez que una versión es publicada, es inmutable. Si se detecta un error, la solución es publicar una nueva versión con el número incrementado.

## Instalación en Modo Editable

Durante el desarrollo del paquete, resulta conveniente poder modificar el código fuente y ver los cambios reflejados inmediatamente, sin necesidad de reconstruir e instalar el paquete cada vez. Esto se logra con la instalación en **modo editable** (también llamada _desarrollo_), mediante el flag `-e`:

```bash
# Instala el paquete en modo editable desde el directorio actual
# Los cambios en el código fuente se reflejan inmediatamente sin reinstalar
pip3 install -e .

# Con dependencias de desarrollo adicionales definidas en pyproject.toml
pip3 install -e ".[dev]"
```

En modo editable, `pip` no copia los archivos del paquete a la ubicación estándar de los paquetes de Python; en su lugar, crea un enlace simbólico al directorio de código fuente. Cualquier modificación en los archivos `.py` queda disponible inmediatamente al importar el paquete, sin necesidad de reinstalar.

## Privacidad: Repositorios Privados y PyPI Interno

No todos los paquetes están destinados a ser publicados en el PyPI público. Una organización puede necesitar distribuir herramientas internas entre sus equipos sin exponer el código al exterior. Para estos casos existen varias alternativas:

**Instalación directa desde un repositorio Git:** `pip` puede instalar un paquete directamente desde una URL de repositorio Git, incluyendo repositorios privados (con autenticación adecuada):

```bash
# Instalar desde un repositorio Git público
pip3 install git+https://github.com/<usuario>/recon-tool.git

# Instalar una rama o tag específica
pip3 install git+https://github.com/<usuario>/recon-tool.git@v1.0.0
```

**Registro privado de paquetes:** Herramientas como `devpi`, `Nexus` o `Artifactory` permiten montar un servidor PyPI privado, al que solo tienen acceso los miembros autorizados de la organización, y desde el cual `pip` puede instalar paquetes exactamente igual que desde el PyPI público.

## Consideraciones de Seguridad en el Ecosistema de Paquetes

Comprender el proceso de distribución de paquetes resulta también valioso desde la perspectiva defensiva, ya que el ecosistema de paquetes de Python ha sido objetivo recurrente de ataques de la cadena de suministro (_supply chain attacks_). Los vectores más comunes incluyen:

El _**typosquatting**_: publicar en PyPI un paquete con un nombre deliberadamente similar a un paquete popular (por ejemplo, `reqeusts` o `colourama` en lugar de `requests` o `colorama`), esperando que algún desarrollador lo instale por error al escribir el nombre con una errata. Una medida defensiva es verificar siempre el nombre exacto del paquete antes de instalarlo y comprobar su popularidad, fecha de creación y repositorio asociado.

La _**dependency confusion**_: un atacante publica en PyPI un paquete con el mismo nombre que un paquete interno privado de una organización, pero con un número de versión mayor. Si `pip` está configurado para buscar también en el PyPI público, puede instalar el paquete malicioso en lugar del interno legítimo. La mitigación consiste en usar un registro privado correctamente configurado con prioridad sobre el público.

El **compromiso de cuentas de mantenedores**: un atacante toma control de la cuenta PyPI del mantenedor de un paquete popular y publica una versión maliciosa. La mitigación pasa por habilitar autenticación de dos factores en todas las cuentas de PyPI, verificar las checksums de los paquetes instalados, y usar herramientas de análisis de dependencias.

Estas consideraciones refuerzan la importancia de auditar regularmente las dependencias de cualquier proyecto, preferir paquetes con mantenimiento activo, y fijar las versiones en `requirements.txt` para garantizar reproducibilidad y evitar instalar versiones inesperadamente modificadas.