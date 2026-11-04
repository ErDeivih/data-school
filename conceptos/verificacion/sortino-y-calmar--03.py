import numpy as np

# Sortino sin retornos negativos en la muestra: el denominador es cero.
r = np.array([0.01, 0.02, 0.03, 0.01])
bajista = np.sqrt((np.minimum(r, 0) ** 2).sum() / r.size)

print(f"bajista {bajista:.4f}")     # -> 0.0000
print(f"Sortino {np.inf if bajista == 0 else r.mean() / bajista:.2f}")   # -> inf
print("sin meses malos el ratio no es enorme: es indefinido")
