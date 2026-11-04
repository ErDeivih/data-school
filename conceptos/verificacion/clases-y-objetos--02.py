class CuentaMala:
    movimientos = []                 # atributo de CLASE: una sola lista para todos

    def __init__(self, titular):
        self.titular = titular

    def ingresar(self, cantidad):
        self.movimientos.append(cantidad)   # busca la lista en la clase, no la crea


class CuentaBuena:
    def __init__(self, titular):
        self.movimientos = []        # cada objeto estrena la suya

    def ingresar(self, cantidad):
        self.movimientos.append(cantidad)


a, b = CuentaMala("Ana"), CuentaMala("Luis")
a.ingresar(30)
b.ingresar(10)
print("mala - lista de a:", a.movimientos, " lista de b:", b.movimientos)  # -> [30, 10] y [30, 10]
print("mala - es la misma lista:", a.movimientos is b.movimientos)          # -> True

c, d = CuentaBuena("Ana"), CuentaBuena("Luis")
c.ingresar(30)
d.ingresar(10)
print("buena - lista de c:", c.movimientos, " lista de d:", d.movimientos)  # -> [30] y [10]
print("buena - es la misma lista:", c.movimientos is d.movimientos)         # -> False
