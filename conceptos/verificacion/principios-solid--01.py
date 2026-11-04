# Abierto y cerrado: anadir una politica no toca el codigo que calcula el total.
class Descuento:
    def importe(self, base):
        raise NotImplementedError     # la clase base no calcula nada: es solo el contrato

class SinDescuento(Descuento):
    def importe(self, base):
        return base

class DiezPorCiento(Descuento):
    def importe(self, base):
        return base * 0.90

class DosPorUno(Descuento):
    def importe(self, base):
        # los primeros 20 euros se pagan enteros; lo que pasa de 20, a mitad de precio
        return base if base <= 20 else 20 + (base - 20) / 2

def total(base, descuento):
    # no hay ningun if sobre el tipo: se llama al mismo metodo y cada clase hace lo suyo
    return round(descuento.importe(base), 2)      # round(x, 2) devuelve un float con dos decimales

print(total(48.0, SinDescuento()))     # -> 48.0
print(total(48.0, DiezPorCiento()))    # -> 43.2
print(total(48.0, DosPorUno()))        # -> 34.0
