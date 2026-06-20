#!/usr/bin/env python3
tope_ventas = 2500
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
    
# Punto de entrada
def main():
    for juego in juegos:
        if ventas_y_stock[juego][0] > tope_ventas:
            sumario(juego)
        
    print(f'\n[+] El total de ventas (sobre el tope) es de: {total_ventas_sobre_tope():,} unidades.'.replace(',', '.'))
    
# Calcular el total de ventas de todos los juegos
total_ventas_sobre_tope = lambda: sum(venta for juego, (venta,_) in ventas_y_stock.items() if ventas_y_stock[juego][0] > tope_ventas)
        
if __name__ == '__main__':
    main()