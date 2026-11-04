from itertools import permutations
from math import factorial

# Cuantos entrelazados admite un programa de 2 hilos con 3 acciones cada uno.
pasos = ["A1", "A2", "A3", "B1", "B2", "B3"]

def valido(orden):
    # Cada hilo conserva el orden de sus propias acciones.
    return (orden.index("A1") < orden.index("A2") < orden.index("A3")
            and orden.index("B1") < orden.index("B2") < orden.index("B3"))

validos = [o for o in permutations(pasos) if valido(o)]
print("entrelazados validos:", len(validos))                      # -> 20
print("formula 6!/(3!*3!):", factorial(6) // factorial(3) ** 2)   # -> 20

# Los que pierden una actualizacion: las dos lecturas antes de las dos escrituras.
malos = [o for o in validos
         if max(o.index("A1"), o.index("B1")) < min(o.index("A3"), o.index("B3"))]
print("pierden una actualizacion:", len(malos))                   # -> 18
