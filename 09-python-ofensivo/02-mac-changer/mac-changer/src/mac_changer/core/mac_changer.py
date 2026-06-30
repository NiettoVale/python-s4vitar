#!/usr/bin/env python3

import subprocess

from rich.console import Console

from mac_changer.utils import is_valid_interface, is_valid_mac, is_root

console = Console()


def change_mac_address(interface: str, mac_address: str) -> None:
    """Valida privilegios, interfaz y MAC, y ejecuta el cambio de dirección MAC.

    Args:
        interface: Nombre de la interfaz de red.
        mac_address: Nueva dirección MAC a asignar.
    """
    if not is_root():
        console.print("[bold red][-][/bold red] Se requieren privilegios de root para cambiar la MAC.")
        return

    errors = []

    if not is_valid_interface(interface):
        errors.append(f"Interfaz inválida: {interface}")

    if not is_valid_mac(mac_address):
        errors.append(f"MAC inválida: {mac_address}")

    if errors:
        for error in errors:
            console.print(f"[bold red][-][/bold red] {error}")
        return

    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.run(["ifconfig", interface, "up"])

    console.print(
        "[bold green][+][/bold green] [cyan]La MAC ha sido cambiada exitosamente[/cyan]"
    )
