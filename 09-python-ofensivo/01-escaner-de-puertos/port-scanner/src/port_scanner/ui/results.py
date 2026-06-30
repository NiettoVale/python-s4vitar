from rich import box
from rich.table import Table

from port_scanner.core import get_service
from port_scanner.ui.console import console


def _build_results_table(ip: str, open_ports: list[int]) -> Table:
    table = Table(
        title=f"[bold green]Puertos abiertos en {ip}[/bold green]",
        box=box.ROUNDED,
        border_style="green",
        show_lines=True,
    )
    table.add_column("Puerto", style="bold cyan", justify="right", width=8)
    table.add_column("Servicio", style="magenta", width=16)
    table.add_column("Estado", justify="center", width=10)

    for port in open_ports:
        table.add_row(str(port), get_service(port), "[bold green]ABIERTO[/bold green]")

    return table


def print_results(ip: str, open_ports: list[int], elapsed_str: str) -> None:
    if open_ports:
        console.print(_build_results_table(ip, open_ports))
        console.print(
            f"\n[bold green]✓[/bold green] [green]{len(open_ports)} puerto(s) abierto(s)[/green]"
        )
    else:
        console.print(
            "[yellow]⚠ No se encontraron puertos abiertos en el rango indicado.[/yellow]"
        )

    console.print(f"[dim]Tiempo de escaneo: {elapsed_str}[/dim]\n")
