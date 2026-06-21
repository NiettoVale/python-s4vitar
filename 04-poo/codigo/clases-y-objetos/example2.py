#!/usr/bin/env python3
class Rectangulo:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

    # Versión sin decorador: así sería un método de instancia normal,
    # que obligaría a llamarlo como rectangulo1.area() (con paréntesis).
    # def area(self):
        # return self.ancho * self.alto

    @property
    # @property convierte al método en un "atributo calculado": permite acceder
    # a rectangulo1.area (SIN paréntesis), como si fuera un atributo normal,
    # aunque por dentro siga ejecutando código (en este caso, una multiplicación).
    def area(self):
        return self.ancho * self.alto

    # Método especial (dunder): define cómo se representa el objeto como texto
    # al hacer print(objeto) o str(objeto). Sin este método, Python mostraría
    # algo genérico como <__main__.Rectangulo object at 0x7fe9c3f36f90>.
    def __str__(self):
        return f'\nPropiedades del rectangulo: [Ancho: {self.ancho}, Alto: {self.alto}]'

    # Método especial (dunder): define qué significa comparar dos objetos
    # Rectangulo con el operador ==. Sin este método, Python compararía
    # por identidad de memoria (si son el MISMO objeto), no por sus valores.
    def __eq__(self, value):
        return self.ancho == value.ancho and self.alto == value.alto

rectangulo1 = Rectangulo(100, 250)
rectangulo2 = Rectangulo(20, 80)

print(rectangulo1)   # invoca automáticamente a __str__()
print(f'[+] El area es: {rectangulo1.area}')   # se accede como atributo, no como método, gracias a @property
print(f'[+] ¿Son Iguales? --> {rectangulo1 == rectangulo2}')   # invoca automáticamente a __eq__()


class Libro:
    def __init__(self, titulo, autor, precio):
        self.titulo = titulo
        self.autor = autor
        self.precio = precio

    def __str__(self):
        return f'El libro "{self.titulo}" fue escrito por "{self.autor}" y cuesta ${self.precio}'

    @staticmethod
    # @staticmethod: este método no usa self ni recibe la instancia ni la clase.
    # Es básicamente una función suelta que vive dentro de Libro porque está
    # temáticamente relacionada con él (clasificar ventas como bestseller o no),
    # aunque no necesite ningún dato propio de un libro en particular.
    def es_bestseller(ventas):
        if ventas >= 5000:
            return 'Este libro es considerado bestseller'
        else:
            return 'Este libro no es considerado bestseller'


mi_libro = Libro('El sistema perdido', 'Francisco', 25)
print(mi_libro)   # invoca automáticamente a __str__()
print(mi_libro.es_bestseller(1000))   # se puede llamar también como Libro.es_bestseller(1000)