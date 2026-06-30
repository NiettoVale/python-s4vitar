# MAC Changer

Herramienta de línea de comandos para cambiar la dirección MAC de una interfaz de red. Desarrollada en Python con [Typer](https://typer.tiangolo.com/) y [Rich](https://github.com/Textualize/rich).

## Requisitos

- Python >= 3.10
- `ifconfig` disponible en el sistema (`net-tools`)
- Privilegios de root para ejecutar el cambio de MAC

## Instalación

### Entorno de desarrollo (editable)

Ideal si quieres modificar el código y ver los cambios al instante:

```bash
pip install -e .
```

Como la herramienta requiere `sudo`, el sistema necesita saber dónde está el ejecutable bajo el entorno de root. Tras la instalación editable, crea un enlace simbólico:

```bash
sudo ln -s $(which mac-changer) /usr/local/bin/mac-changer
```

De esta forma puedes seguir editando el código con `pip install -e .` y ejecutar la herramienta con `sudo` sin problemas.

### Instalación global con pipx

Si solo quieres usar la herramienta sin modificarla, `pipx` es la opción más limpia: aísla la aplicación en su propio entorno virtual y la expone globalmente:

```bash
sudo pipx install .
```

## Uso

```bash
sudo mac-changer -i <interfaz> -m <mac>
```

| Opción | Descripción |
|--------|-------------|
| `-i`, `--interface` | Nombre de la interfaz de red (ej. `eth0`, `wlan0`, `enp2s0`) |
| `-m`, `--mac` | Nueva dirección MAC en formato `XX:XX:XX:XX:XX:XX` |

### Ejemplo

```bash
sudo mac-changer -i eth0 -m 00:11:22:33:44:55
```

### Interfaces soportadas

| Patrón | Ejemplos | Tipo |
|--------|----------|------|
| `eth\d+` | `eth0`, `eth1` | Ethernet clásico |
| `ens\d+` | `ens3`, `ens33` | Ethernet systemd (slot) |
| `eno\d+` | `eno1` | Ethernet systemd (onboard) |
| `enp\d+s\d+` | `enp2s0`, `enp3s0f0` | Ethernet systemd (PCI) |
| `wlan\d+` | `wlan0`, `wlan1` | WiFi clásico |
| `wlp\d+s\d+` | `wlp2s0` | WiFi systemd (PCI) |
| `lo` | `lo` | Loopback |

## Utilidades para pruebas

Para verificar el cambio de MAC puedes usar la herramienta `macchanger`:

```bash
# Ver el listado de OUIs disponibles
macchanger -l

# Ver la MAC actual y la permanente de una interfaz
macchanger -s <interfaz>
```

## Estructura del proyecto

```
src/mac_changer/
├── core/
│   └── mac_changer.py     # Lógica principal: validación y cambio de MAC
├── interface/
│   └── cli.py             # CLI construida con Typer
└── utils/
    ├── validators.py      # Validaciones de MAC e interfaz
    └── system.py          # Comprobación de privilegios de root
```
