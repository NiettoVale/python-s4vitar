#!/usr/bin/env python3
from time import sleep
import os

print("""
====================================
        🎮 GameInfo System
====================================

Bienvenido.
Este sistema analiza ventas de videojuegos
y genera reportes filtrados por un umbral.

------------------------------------
""")

tope_ventas = int(input("Ingrese el tope de ventas: "))

print("\n⏳ Procesando datos...\n")
sleep(2)
os.system('cls' if os.name == 'nt' else 'clear')

juegos = [
    "Super Mario Bros",
    "Zelda: Breath of the Wild",
    "Cyberpunk 2077",
    "Final Fantasy VII",
    "Elden Ring",
    "Stardew Valley",
    "Minecraft",
    "Hollow Knight",
    "Persona 5 Royal"
]

# Géneros
generos = {
    "Super Mario Bros": "Aventura",
    "Zelda: Breath of the Wild": "Aventura",
    "Cyberpunk 2077": "Rol",
    "Final Fantasy VII": "Rol",
    "Elden Ring": "Rol",
    "Stardew Valley": "Simulación",
    "Minecraft": "Sandbox",
    "Hollow Knight": "Metroidvania",
    "Persona 5 Royal": "Rol"
}

# Ventas y Stock
ventas_y_stock = {
    "Super Mario Bros": (400, 200),
    "Zelda: Breath of the Wild": (600, 20),
    "Cyberpunk 2077": (60, 120),
    "Final Fantasy VII": (924, 3),
    "Elden Ring": (1500, 50),
    "Stardew Valley": (3000, 500),
    "Minecraft": (5000, 1000),
    "Hollow Knight": (800, 150),
    "Persona 5 Royal": (450, 80)
}

# Clientes
clientes = {
    "Super Mario Bros": {"Marcelo", "Hackermate", "Hackavis", "Securiters", "Lobotec"},
    "Zelda: Breath of the Wild": {"Hackermate", "Hackavis", "Lucía", "Manolo", "Pepe"},
    "Cyberpunk 2077": {"Hackermate", "Lobotec", "Pepe", "Raquel", "Albert"},
    "Final Fantasy VII": {"Lucía", "Manolo", "Pepe", "Securiters", "Patricia", "Moisés"},
    "Elden Ring": {"Lucía", "GamerPro99", "Moisés", "Ana", "Carlos"},
    "Stardew Valley": {"Raquel", "Patricia", "Valeria", "Pepe", "Sofía"},
    "Minecraft": {"Creep", "Marcelo", "Albert", "Lucía", "Diego"},
    "Hollow Knight": {"Hackavis", "GamerPro99", "Julia", "Marcos"},
    "Persona 5 Royal": {"Securiters", "Ren", "Ana", "Pedro"}
}

# Sumario
def sumario(juego):    
    print(f"\n[i] Resumen de \"{juego}\"\n")
    print(f"\t[+] Genero: {generos[juego]}")
    print(f"\t[+] Total de ventas: {ventas_y_stock[juego][0]} unidades")
    print(f"\t[+] Stock actual: {ventas_y_stock[juego][1]} unidades")
    print(f"\t[+] Clientes que adquirieron el juego: {', '.join(clientes[juego])}")
    
# Encabezado reporte
def encabezado_reporte():
    print("\n" + "=" * 45)
    print("📊 GAMEINFO - REPORTE DE VENTAS")
    print("=" * 45)
    print("\n🔎 Analizando juegos con ventas sobre el tope...\n")
    
# Punto de entrada
def main():
    encabezado_reporte()
    
    encontrados = False
    
    for juego in juegos:
        if ventas_y_stock[juego][0] > tope_ventas:
            sumario(juego)
            encontrados = True
    
    if not encontrados:
        print("No se encontraron juegos que superen el tope.\n")
    
    print("\n" + "-" * 45)
    print(f"Total (sobre el tope): {total_ventas_sobre_tope():,} unidades")
    print("-" * 45)
    
    
# Calcular el total de ventas de todos los juegos
total_ventas_sobre_tope = lambda: sum(venta for juego, (venta,_) in ventas_y_stock.items() if ventas_y_stock[juego][0] > tope_ventas)
        
if __name__ == '__main__':
    main()