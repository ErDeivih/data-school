# El caso clasico de violacion de Liskov: el cuadrado que hereda del rectangulo.
class Rectangulo:
    def __init__(self, ancho, alto):
        self.ancho, self.alto = ancho, alto
    def set_ancho(self, valor): self.ancho = valor
    def set_alto(self, valor):  self.alto = valor
    def area(self): return self.ancho * self.alto

class Cuadrado(Rectangulo):
    def __init__(self, lado):
        super().__init__(lado, lado)      # super() llama al constructor del padre con los dos lados iguales
    def set_ancho(self, valor): self.ancho = self.alto = valor   # mantiene el cuadrado...
    def set_alto(self, valor):  self.ancho = self.alto = valor   # ...y rompe al padre

def area_tras_ajustes(rect):
    """Invariante del padre: tras fijar 5 de ancho y 4 de alto, el area es 20."""
    # no comprueba el tipo: acepta cualquier subtipo, que es justo lo que promete LSP
    rect.set_ancho(5)
    rect.set_alto(4)
    return rect.area()

print("rectangulo 2x3:", area_tras_ajustes(Rectangulo(2, 3)))   # -> 20
print("cuadrado de lado 2:", area_tras_ajustes(Cuadrado(2)))    # -> 16
