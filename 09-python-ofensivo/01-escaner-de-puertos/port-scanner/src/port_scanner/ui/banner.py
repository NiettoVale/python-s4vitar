from rich.panel import Panel
from rich.text import Text

from port_scanner.ui.console import console


def print_banner() -> None:
    title = Text("⚡ PORT SCANNER", style="bold cyan")
    console.print(Panel(title, border_style="cyan", expand=False, padding=(0, 4)))


def print_target_info(ip: str, start: int, end: int) -> None:
    console.print(f"\n  [bold]Objetivo :[/bold] [yellow]{ip}[/yellow]")
    console.print(f"  [bold]Rango    :[/bold] [cyan]{start}[/cyan] → [cyan]{end}[/cyan]\n")
