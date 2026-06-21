#!/usr/bin/env python3

# =========================
# CLASES
# =========================

class Animal:
    """Representa un animal simple, identificado por su nombre y su tipo (especie)."""

    def __init__(self, nombre, tipo):
        # __init__ es el constructor: se ejecuta automáticamente al crear cada objeto Animal.
        # 'self' es la referencia a la instancia que se está creando en ese momento.
        self.nombre = nombre   # atributo de instancia: propio de cada Animal creado
        self.tipo = tipo       # atributo de instancia: propio de cada Animal creado

    def descripcion(self):
        # Método de instancia: utiliza self para acceder a los atributos de ESTE objeto puntual.
        print(f'{self.nombre} es un {self.tipo}.')


class Persona:
    """Representa a una persona, identificada por su nombre y su edad."""

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludo(self):
        # Genera un saludo personalizado usando los atributos propios de la instancia.
        print(f'Hola, me llamo {self.nombre} y tengo {self.edad} años.')


class CuentaBancaria:
    """Representa una cuenta bancaria simple, con operaciones de depósito y extracción."""

    def __init__(self, cuenta, nombre, dinero=0):
        # 'dinero' tiene un valor por defecto (0), por lo que es opcional al crear la cuenta.
        self.cuenta = cuenta   # número de cuenta
        self.nombre = nombre   # titular de la cuenta
        self.dinero = dinero   # saldo actual, inicia en 0 salvo que se indique otro valor

    def mostrar_resumen(self):
        """Imprime por consola un resumen formateado con los datos actuales de la cuenta."""
        print('\n' + '=' * 45)
        print('          RESUMEN DE LA CUENTA')
        print('=' * 45)
        print(f'Titular         : {self.nombre}')
        print(f'N.º de cuenta   : {self.cuenta}')
        print(f'Saldo actual    : ${self.dinero:.2f}')
        print('=' * 45)

    def depositar_dinero(self, dinero_a_depositar):
        """Suma el monto indicado al saldo actual de la cuenta y muestra el detalle de la operación."""
        print('\n' + '=' * 45)
        print('            OPERACIÓN: DEPÓSITO')
        print('=' * 45)
        print(f'Titular             : {self.nombre}')
        print(f'Saldo anterior      : ${self.dinero:.2f}')
        print(f'Monto a depositar   : ${dinero_a_depositar:.2f}')
        self.dinero += dinero_a_depositar   # se actualiza el estado (saldo) de ESTA instancia
        print('-' * 45)
        print('✅ Depósito realizado correctamente.')
        print(f'Nuevo saldo         : ${self.dinero:.2f}')
        print('=' * 45)

    def extraer_dinero(self, dinero_a_extraer):
        """Resta el monto indicado del saldo, siempre que existan fondos suficientes."""
        print('\n' + '=' * 45)
        print('            OPERACIÓN: EXTRACCIÓN')
        print('=' * 45)
        if dinero_a_extraer > self.dinero:
            # Validación de fondos: evita que el saldo quede en negativo
            print('❌ Fondos insuficientes.')
            print(f'Saldo disponible    : ${self.dinero:.2f}')
        else:
            print(f'Saldo anterior      : ${self.dinero:.2f}')
            print(f'Monto a extraer     : ${dinero_a_extraer:.2f}')
            self.dinero -= dinero_a_extraer   # se actualiza el estado (saldo) de ESTA instancia
            print('-' * 45)
            print('✅ Extracción realizada correctamente.')
            print(f'Nuevo saldo         : ${self.dinero:.2f}')
        print('=' * 45)


# =========================
# PERSONA
# =========================
print('\nPERSONA')
print('-' * 45)

# Se crea una instancia (objeto) de la clase Persona
francisco = Persona('Francisco', 23)
francisco.saludo()

# type() permite confirmar que 'francisco' es, efectivamente, un objeto de tipo Persona
print(f'Tipo de la variable "francisco": {type(francisco)}')

# =========================
# ANIMALES
# =========================
print('\nANIMALES')
print('-' * 45)

# Se crean dos instancias independientes de la clase Animal, cada una con su propio estado
gato = Animal('Tijuana', 'gato')
perro = Animal('Clarita', 'perro')
gato.descripcion()
perro.descripcion()

# =========================
# CUENTA BANCARIA
# =========================
print('\nCUENTA BANCARIA')
print('-' * 45)

# Se crea una cuenta bancaria con saldo inicial 0 (no se especifica el parámetro 'dinero')
zeta = CuentaBancaria('123566456', 'Zeta')
zeta.mostrar_resumen()

zeta.depositar_dinero(2000)   # saldo pasa de 0 a 2000
zeta.extraer_dinero(500)      # saldo pasa de 2000 a 1500
zeta.extraer_dinero(5000)     # excede el saldo disponible (1500): se rechaza la operación