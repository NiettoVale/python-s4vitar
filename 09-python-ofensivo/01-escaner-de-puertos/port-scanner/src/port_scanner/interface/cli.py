#!/usr/bin/env python3

import typer

from port_scanner.ui import print_banner, print_results, print_target_info, run_scan

app = typer.Typer(help="Herramienta de escaneo de puertos TCP.")


@app.command()
def main(
    ip: str = typer.Argument(..., help="IP objetivo a escanear"),
    start: int = typer.Option(1, "--start", "-s", help="Puerto inicial"),
    end: int = typer.Option(1000, "--end", "-e", help="Puerto final"),
    all_ports: bool = typer.Option(
        False, "--all", "-a", help="Escanear todos los puertos (1-65535)"
    ),
):
    if all_ports:
        start, end = 1, 65535

    print_banner()
    print_target_info(ip, start, end)

    open_ports, elapsed_str = run_scan(ip, start, end)
    print_results(ip, open_ports, elapsed_str)


if __name__ == "__main__":
    app()
