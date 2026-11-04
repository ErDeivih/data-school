import numpy as np

# Dependencia perfecta y no lineal: x de -3 a 3, y = x^2.
x = np.arange(-3, 4, dtype=float)
y = x ** 2
print(f"covarianza(x, x^2)  = {np.cov(x, y, ddof=1)[0, 1]:.4f}")   # -> 0.0000
print(f"correlacion(x, x^2) = {np.corrcoef(x, y)[0, 1]:.4f}")      # -> 0.0000

# Relacion lineal decreciente: la correlacion llega al minimo posible.
w = -np.arange(6, dtype=float)
print(f"correlacion lineal negativa = {np.corrcoef(np.arange(6.0), w)[0, 1]:.4f}")  # -> -1.0000
