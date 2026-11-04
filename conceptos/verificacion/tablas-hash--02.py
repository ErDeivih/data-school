# Modulo primo frente a potencia de 2: la misma familia de claves, dos repartos.
claves = [1024, 2048, 3072, 4096, 5120, 6144]   # todas multiplos de 1024

def colisiones(valores, m):
    """Cuantos valores comparten cubo con otro: 0 seria un reparto perfecto."""
    cuenta = {}
    for v in valores:
        cuenta[v % m] = cuenta.get(v % m, 0) + 1
    return sum(c - 1 for c in cuenta.values() if c > 1)

print("modulo 1024, potencia de 2  colisiones:", colisiones(claves, 1024))  # -> 5
print("modulo 1009, primo         colisiones:", colisiones(claves, 1009))  # -> 0
print("cubos ocupados con 1024:", len({k % 1024 for k in claves}))         # -> 1
print("cubos ocupados con 1009:", len({k % 1009 for k in claves}))         # -> 6
