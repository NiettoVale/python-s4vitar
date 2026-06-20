#!/usr/bin/env python3

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

mi_juego = "Minecraft"

# Sumario
print(f"\n[i] Resumen de \"{mi_juego}\"\n")
print(f"\t[+] Genero: {generos[mi_juego]}")
print(f"\t[+] Total de ventas: {ventas_y_stock[mi_juego][0]} unidades")
print(f"\t[+] Stock actual: {ventas_y_stock[mi_juego][1]} unidades")
print(f"\t[+] Clientes que adquirieron el juego: {', '.join(clientes[mi_juego])}")