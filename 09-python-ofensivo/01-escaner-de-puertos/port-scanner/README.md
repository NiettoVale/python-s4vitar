# Port Scanner

Herramienta CLI para escanear puertos TCP, construida como proyecto integrador del curso de Python Ofensivo.

## Instalación

Requiere Python 3.10+.

```bash
pip install .
```

Esto registra el comando `port-scanner` en el entorno activo, permitiendo ejecutarlo desde cualquier directorio.

## Uso

```
port-scanner [OPTIONS] IP
```

### Argumentos

| Argumento | Descripción |
|-----------|-------------|
| `IP` | Dirección IP objetivo (requerido) |

### Opciones

| Opción | Alias | Default | Descripción |
|--------|-------|---------|-------------|
| `--start` | `-s` | `1` | Puerto inicial del rango |
| `--end` | `-e` | `1000` | Puerto final del rango |
| `--all` | `-a` | `False` | Escanea todos los puertos (1-65535) |

### Ejemplos

```bash
# Escaneo con rango por defecto (1-1000)
port-scanner 192.168.1.1

# Escaneo de un rango personalizado
port-scanner 192.168.1.1 --start 20 --end 100

# Escaneo completo de todos los puertos
port-scanner 192.168.1.1 --all
```

## Estructura del proyecto

```
port-scanner/
├── pyproject.toml
└── src/
    └── port_scanner/
        ├── core/
        │   ├── __init__.py
        │   └── port_scanner.py     # Lógica de escaneo TCP con sockets
        ├── interface/
        │   ├── __init__.py
        │   └── cli.py              # Punto de entrada: definición del comando con typer
        └── ui/
            ├── __init__.py
            ├── banner.py           # Banner y datos del objetivo
            ├── console.py          # Instancia compartida de Console (rich)
            ├── progress.py         # Barra de progreso y lógica de escaneo
            └── results.py          # Tabla de resultados
```

## Dependencias

- [`typer`](https://typer.tiangolo.com/) — parseo de argumentos y opciones CLI
- [`rich`](https://rich.readthedocs.io/) — output con colores, tablas y barra de progreso
- `socket` (stdlib) — conexiones TCP para detectar puertos abiertos

## Cómo funciona

El escáner intenta abrir una conexión TCP (`SOCK_STREAM`) a cada puerto del rango indicado. Si la conexión se establece, el puerto está abierto. Si se agota el timeout (1 segundo) o la conexión es rechazada, el puerto está cerrado o filtrado.

Una vez terminado el escaneo se muestra una tabla con el número de puerto, el servicio asociado (via `socket.getservbyport`) y su estado.
