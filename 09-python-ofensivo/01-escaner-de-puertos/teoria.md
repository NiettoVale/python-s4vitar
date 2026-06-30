En este proyecto se va a construir un escaner de puertos, aplicando todo lo que si vio hasta el momento.
Este se va dividir en diversas etapas, donde se va ir mejorando el escaner.

---

## Fase 1: creacion del proyecto

Se creo una carpeta llamada `port-scanner`, la cual va actuar como carpeta raiz del proyecto, dentro se creo la carpeta `src/port_scanner` la cual va almacenar todo el proyecto, esto se hace asi por convenciones del fichero `pyproject.toml` el cual nos va permitir crear este proyecto como un instalador global para poder ejecutar `port-scanner` en lugar de ejecutar el fichero con `python3`.

### pyproject.toml

Este fichero es el corazon de la configuracion del proyecto. Define el nombre del paquete, la version, las dependencias y el punto de entrada del comando CLI:

```toml
[project]
name = "port-scanner"
version = "0.0.1"
requires-python = ">=3.10"

dependencies = [
    "typer>=0.16",
    "rich>=14.0",
]

[project.scripts]
port-scanner = "port_scanner.interface.cli:app"
```

La clave es la seccion `[project.scripts]`: al hacer `pip install .`, Python registra el comando `port-scanner` que apunta directamente al objeto `app` de `cli.py`. Esto es lo que permite ejecutar la herramienta como un comando global.

El build backend usado es `hatchling`, una alternativa moderna a `setuptools`.

### Estructura del proyecto

```plaintext
port-scanner/
├── pyproject.toml
└── src/
    └── port_scanner/
        ├── __init__.py
        ├── core/
        │   ├── __init__.py
        │   └── port_scanner.py
        ├── interface/
        │   ├── __init__.py
        │   └── cli.py
        └── ui/
            ├── __init__.py
            ├── banner.py
            ├── console.py
            ├── progress.py
            └── results.py
```

El proyecto se organiza en tres capas bien separadas:

- **`core/`** — logica pura de red, sin nada de presentacion
- **`interface/`** — punto de entrada CLI, parseo de argumentos
- **`ui/`** — todo lo relacionado a como se muestra la informacion en la terminal

---

## Fase 2: logica de escaneo con sockets (`core/port_scanner.py`)

El modulo `core` es donde vive la logica de bajo nivel. Se usan sockets TCP para intentar conectarse a cada puerto:

```python
import socket

def create_socket() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    return s

def scan_port(host: str, port: int) -> bool:
    s = create_socket()
    try:
        s.connect((host, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    finally:
        s.close()
```

**Conceptos aplicados:**
- `AF_INET` + `SOCK_STREAM` crea un socket TCP/IPv4.
- `settimeout(1)` hace que la conexion espere maximo 1 segundo antes de considerarse fallida.
- `connect()` intenta establecer la conexion: si tiene exito el puerto esta abierto, si lanza `ConnectionRefusedError` o `socket.timeout` esta cerrado o filtrado.
- El bloque `finally` garantiza que el socket siempre se cierra, incluso si hay un error.

Ademas, `get_service` usa `socket.getservbyport()` para resolver el nombre del servicio asociado a un puerto conocido (ej: 80 → `http`, 22 → `ssh`):

```python
def get_service(port: int) -> str:
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"
```

El `__init__.py` de `core` re-exporta lo que la capa de UI necesita usar:

```python
from .port_scanner import get_service as get_service
from .port_scanner import scan_port as scan_port
```

---

## Fase 3: interfaz CLI con typer (`interface/cli.py`)

Se uso la libreria `typer` para definir el comando principal. Typer infiere automaticamente los tipos y genera el `--help` a partir de los type hints y los parametros:

```python
import typer

app = typer.Typer(help="Herramienta de escaneo de puertos TCP.")

@app.command()
def main(
    ip: str = typer.Argument(..., help="IP objetivo a escanear"),
    start: int = typer.Option(1, "--start", "-s", help="Puerto inicial"),
    end: int = typer.Option(1000, "--end", "-e", help="Puerto final"),
    all_ports: bool = typer.Option(False, "--all", "-a", help="Escanear todos los puertos (1-65535)"),
):
    if all_ports:
        start, end = 1, 65535

    print_banner()
    print_target_info(ip, start, end)
    open_ports, elapsed_str = run_scan(ip, start, end)
    print_results(ip, open_ports, elapsed_str)
```

**Conceptos aplicados:**
- `typer.Argument` define un argumento posicional obligatorio (el `...` indica que es requerido).
- `typer.Option` define flags opcionales con valor por defecto.
- El flag `--all` sobreescribe `start` y `end` para forzar el rango completo 1-65535.
- El flujo es lineal: banner → info del objetivo → escaneo → resultados.

---

## Fase 4: presentacion con rich (`ui/`)

El modulo `ui` agrupa todo lo visual. Se uso la libreria `rich` para darle color y estructura al output en la terminal.

### `console.py` — instancia compartida

```python
from rich.console import Console
console = Console()
```

Se crea una unica instancia de `Console` que todos los modulos de `ui` importan. Esto evita crear multiples instancias y asegura que todo el output pase por el mismo canal.

### `banner.py` — banner y datos del objetivo

```python
from rich.panel import Panel
from rich.text import Text

def print_banner() -> None:
    title = Text("⚡ PORT SCANNER", style="bold cyan")
    console.print(Panel(title, border_style="cyan", expand=False, padding=(0, 4)))

def print_target_info(ip: str, start: int, end: int) -> None:
    console.print(f"\n  [bold]Objetivo :[/bold] [yellow]{ip}[/yellow]")
    console.print(f"  [bold]Rango    :[/bold] [cyan]{start}[/cyan] → [cyan]{end}[/cyan]\n")
```

`rich` usa markup entre corchetes `[bold cyan]...[/bold cyan]` para aplicar estilos, similar a HTML pero para la terminal.

### `progress.py` — barra de progreso durante el escaneo

```python
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
import time

def run_scan(ip: str, start: int, end: int) -> tuple[list[int], str]:
    open_ports: list[int] = []
    start_time = time.monotonic()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TextColumn("[dim]{task.completed}/{task.total} puertos[/dim]"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("[green]Escaneando...", total=end - start + 1)
        for port in range(start, end + 1):
            if scan_port(ip, port):
                open_ports.append(port)
            progress.advance(task)

    return open_ports, format_elapsed(time.monotonic() - start_time)
```

**Conceptos aplicados:**
- `Progress` de rich acepta columnas configurables: spinner, texto, barra, porcentaje y contador.
- `transient=True` hace que la barra desaparezca al terminar, dejando solo los resultados.
- `time.monotonic()` se usa en lugar de `time.time()` para medir duraciones porque no se ve afectado por cambios del reloj del sistema.
- `format_elapsed` convierte los segundos al formato `HH:MM:SS`.

### `results.py` — tabla de resultados

```python
from rich.table import Table
from rich import box

def print_results(ip: str, open_ports: list[int], elapsed_str: str) -> None:
    if open_ports:
        console.print(_build_results_table(ip, open_ports))
        console.print(f"\n[bold green]✓[/bold green] [green]{len(open_ports)} puerto(s) abierto(s)[/green]")
    else:
        console.print("[yellow]⚠ No se encontraron puertos abiertos en el rango indicado.[/yellow]")

    console.print(f"[dim]Tiempo de escaneo: {elapsed_str}[/dim]\n")
```

La tabla usa `box.ROUNDED` para bordes redondeados y muestra tres columnas: puerto, servicio y estado.

---

## Como instalar y ejecutar

```bash
# Desde la carpeta port-scanner/
pip install .

# Uso basico
port-scanner 192.168.1.1

# Rango personalizado
port-scanner 192.168.1.1 --start 20 --end 443

# Todos los puertos
port-scanner 192.168.1.1 --all
```

---

## Librerias utilizadas

| Libreria | Uso |
|----------|-----|
| `socket` (stdlib) | Conexiones TCP para detectar puertos abiertos |
| `time` (stdlib) | Medicion del tiempo de escaneo |
| `typer` | Definicion del comando CLI con tipos y `--help` automatico |
| `rich` | Colores, tablas, barra de progreso y paneles en la terminal |
