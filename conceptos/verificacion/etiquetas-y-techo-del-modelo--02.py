import numpy as np

rng = np.random.default_rng(7)
n, C = 200_000, 2
y = rng.integers(0, C, n)
m = 0.05                                        # 5 % de ejemplos con etiqueta en conflicto
ambiguo = rng.random(n) < m
y_etiquetada = np.where(ambiguo, rng.integers(0, C, n), y)

techo = 1 - m + m / C                           # lo mejor que puede hacer cualquier modelo
empirico = ((~ambiguo).sum() + ambiguo.sum() / C) / n
acuerdo = (y_etiquetada == y).mean()

print(f"techo teorico   {techo:.4f}")           # -> 0.9750
print(f"techo empirico  {empirico:.4f}")        # -> 0.9752
print(f"acuerdo con la verdad  {acuerdo:.4f}")  # -> 0.9753
