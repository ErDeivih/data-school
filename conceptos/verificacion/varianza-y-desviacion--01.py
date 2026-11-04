import numpy as np

x = np.arange(1, 7, dtype=float)          # un dado justo, valores equiprobables
var = (x ** 2).mean() - x.mean() ** 2     # E[X^2] - (E[X])^2

print(f"E[X^2]       = {(x ** 2).mean():.4f}")   # -> 15.1667
print(f"Var(X)       = {var:.4f}")               # -> 2.9167
print(f"Desv. tipica = {np.sqrt(var):.4f}")      # -> 1.7078
print(f"Var(3X + 10) = {(3 * x + 10).var():.4f}")  # -> 26.2500
