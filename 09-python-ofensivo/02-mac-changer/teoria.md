Este proyecto va servir para poder cambiar la MAC de una interfaz de red. Como se vino trabajando en proyectos anteriores, lo vamos a dividir por fases.

---

## Fase 1: Validaciones

En esta fase se crearon dos funciones en el módulo `utils/validators.py`:

- `is_valid_mac(mac: str) -> bool`: valida que la MAC tenga el formato `XX:XX:XX:XX:XX:XX` usando una expresión regular.
- `is_valid_interface(interface: str) -> bool`: valida que la interfaz de red tenga un formato conocido (ej. `eth0`, `ens3`, `wlan0`) mediante regex.

Ambas funciones se exponen en `utils/__init__.py` para que el resto del proyecto las importe directamente desde el paquete.

---

## Fase 2: Lógica de negocio (core)

En el módulo `core/mac_changer.py` se implementó la función `change_mac_address(interface, mac_address)`:

- Usa las validaciones del paquete `utils` para comprobar si la interfaz y la MAC son válidas.
- Acumula todos los errores encontrados en una lista y los muestra por pantalla si los hay.
- Si ambos valores son válidos, imprime confirmación de cada uno.

La función se expone a través de `core/__init__.py`.

---

## Fase 3: Interfaz de línea de comandos (CLI)

En `interface/cli.py` se construyó la CLI usando **Typer**:

- El comando principal `main` acepta dos opciones obligatorias: `-i/--interface` y `-m/--mac`.
- Delega directamente en `change_mac_address` del paquete `core`.
- La herramienta se registra como script instalable `mac-changer` en `pyproject.toml`, con punto de entrada `mac_changer.interface.cli:app`.

---

## Fase 4: Mejoras visuales con Rich

Se integró la librería **Rich** para mejorar la salida por pantalla:

- **`core/mac_changer.py`**: se sustituyeron los `print()` por `console.print()` de Rich.
  - Los errores se muestran en **rojo** con prefijo `[-]`.
  - Los mensajes de éxito se muestran en **verde** con prefijo `[+]` y los valores resaltados en **cyan**.

- **`interface/cli.py`**: se añade un `Panel` de Rich al inicio de la ejecución con el título de la herramienta y borde en cyan.

## Fase 5: Cambio de MAC

Se extendió `change_mac_address` en `core/mac_changer.py` para que, tras pasar las validaciones, ejecute el cambio real usando `subprocess.run()` con una lista de argumentos (nunca `shell=True`), lo que previene inyección de comandos.

Los tres pasos ejecutados son:

```
ifconfig <interfaz> down
ifconfig <interfaz> hw ether <nueva_mac>
ifconfig <interfaz> up
```

Al finalizar, se muestra un mensaje de éxito por pantalla mediante Rich. Si alguna validación falla, la función aborta antes de tocar la interfaz.

---

## Fase 6: Validación de privilegios de root

Se añadió el módulo `utils/system.py` con la función `is_root() -> bool`, que comprueba si el proceso se está ejecutando como root mediante `os.geteuid() == 0`.

Esta comprobación se realiza en `change_mac_address` como primer paso, antes incluso de validar la interfaz o la MAC, ya que sin privilegios de root los comandos `ifconfig` fallarían. Si no se tiene root, se muestra un error en rojo y la función aborta inmediatamente.

La función se exporta desde `utils/__init__.py` junto al resto de utilidades.

### Dependencias del proyecto (`pyproject.toml`)

| Paquete | Versión mínima |
| ------- | -------------- |
| typer   | >=0.16         |
| rich    | >=14.0         |

El proyecto usa **Hatchling** como build backend y requiere Python >= 3.10.
