import time

from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from port_scanner.core import scan_port
from port_scanner.ui.console import console


def format_elapsed(seconds: float) -> str:
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


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
