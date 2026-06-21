#!/usr/bin/env python3

# Static Methods
class Calculadora:
    # Todos los métodos de esta clase son @staticmethod porque ninguno necesita
    # acceder a self ni a cls: son simplemente funciones matemáticas agrupadas
    # dentro de la clase por organización temática. Por eso se invocan
    # directamente sobre la clase: Calculadora.suma(...), sin crear una instancia.

    @staticmethod
    def suma(a, b):
        return a + b

    @staticmethod
    def resta(a, b):
        return a - b

    @staticmethod
    def multiplicacion(a, b):
        return a * b

    @staticmethod
    def division(a, b):
        if b != 0:
            return a // b
        else:
            return '[-] Error!! No se puede dividir por cero.'


class Automovil:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    @classmethod
    # Método de clase usado como "factory" (constructor alternativo): en vez de
    # llamar a Automovil(marca, modelo) indicando ambos valores a mano, este
    # método arma la instancia fijando 'modelo' siempre como "deportivo".
    # 'cls' hace referencia a la propia clase Automovil, por lo que cls(marca, "deportivo")
    # equivale a escribir Automovil(marca, "deportivo").
    def deportivos(cls, marca):
        return cls(marca, "deportivo")

    def __str__(self):
        return f'La marca "{self.marca}" es un modelo "{self.modelo}"'


class Estudiante:
    # Atributo de CLASE (no de instancia): existe una sola vez y es compartido
    # por todos los objetos Estudiante, a diferencia de self.nombre o self.edad,
    # que cada instancia tiene por separado. Se usa aquí como un registro global.
    estudiantes = []

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

        # Cada vez que se crea un Estudiante, se lo agrega automáticamente
        # a la lista compartida por toda la clase.
        Estudiante.estudiantes.append(self)

    @staticmethod
    # No necesita self ni cls: es una validación pura que solo depende del
    # parámetro 'edad' que recibe, sin importar a qué estudiante pertenezca.
    def es_mayor_de_edad(edad):
        if edad >= 18:
            return True
        return False

    @classmethod
    # Método de clase usado como "constructor controlado": antes de crear el
    # objeto, valida una condición de negocio (ser mayor de edad) reutilizando
    # el método estático es_mayor_de_edad(). Si la condición no se cumple,
    # la función termina sin devolver nada (devuelve None de forma implícita,
    # y por lo tanto no se crea ni se registra ningún estudiante).
    def crear_estudiante(cls, nombre, edad):
        if cls.es_mayor_de_edad(edad):
            return cls(nombre, edad)

    @staticmethod
    # Aunque accede a Estudiante.estudiantes, lo hace usando el nombre de la
    # clase de forma explícita (no a través de self/cls), por eso puede
    # definirse como estático: no depende de qué instancia particular se use
    # para llamarlo, ya que de hecho se invoca directamente sobre la clase.
    def mostrar_estudiante():
        if not Estudiante.estudiantes:
            print("\nNo hay estudiantes registrados.\n")
            return

        print("\n" + "=" * 45)
        print("LISTADO DE ESTUDIANTES".center(45))
        print("=" * 45)
        print(f"{'Legajo':<10}{'Nombre':<20}{'Edad':<10}")
        print("-" * 45)
        # enumerate(..., start=1) genera un número de legajo correlativo,
        # empezando en 1 en lugar de 0, para cada estudiante registrado
        for i, estudiante in enumerate(Estudiante.estudiantes, start=1):
            print(f"{i:<10}{estudiante.nombre:<20}{estudiante.edad:<10}")
        print("=" * 45)
        print(f"Total de estudiantes: {len(Estudiante.estudiantes)}")
        print("=" * 45)


print('\nStatic Methods\n')
# Se invocan directamente sobre la clase, sin crear ninguna instancia de Calculadora
print(Calculadora.suma(2, 3))
print(Calculadora.resta(20, 13))
print(Calculadora.multiplicacion(2, 10))
print(Calculadora.division(8, 0))

print('\nClass Methods\n')
boreal = Automovil('Renault Boreal', 'SUV\'')   # constructor normal: se especifica el modelo
ferrari = Automovil.deportivos("Ferrari")       # constructor alternativo: el modelo queda fijo
print(boreal)
print(ferrari)

print('\nMezlca de ambos casos\n')
# Todos mayores de edad: se crean y se agregan al registro estudiantes[]
Estudiante.crear_estudiante('Francisco', 23)
Estudiante.crear_estudiante('Valentina', 14)
Estudiante.crear_estudiante('Zeta', 22)
Estudiante.crear_estudiante('Json', 26)
Estudiante.crear_estudiante('Tania', 22)
Estudiante.mostrar_estudiante()