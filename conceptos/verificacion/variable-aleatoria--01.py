from collections import Counter
from itertools import product

# X = suma de dos dados. Enumeramos los 36 resultados equiprobables, sin simular nada.
resultados = Counter(a + b for a, b in product(range(1, 7), repeat=2))
total = sum(resultados.values())

print(f"P(X = 7)   = {resultados[7] / total:.4f}")     # -> 0.1667
print(f"P(X <= 4)  = {sum(v for k, v in resultados.items() if k <= 4) / total:.4f}")  # -> 0.1667
print(f"P(X >= 11) = {sum(v for k, v in resultados.items() if k >= 11) / total:.4f}")  # -> 0.0833

# La masa suma 1: es la comprobacion de que la distribucion esta completa.
print("suma de la masa =", sum(resultados.values()) / total)   # -> 1.0
