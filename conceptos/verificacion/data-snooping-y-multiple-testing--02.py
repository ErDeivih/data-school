import numpy as np
from statistics import NormalDist

Z = NormalDist()
rng = np.random.default_rng(0)
m, n = 1000, 250        # 1000 estrategias sin alpha, 250 dias cada una
r = rng.normal(0.0, 0.01, size=(m, n))
t = r.mean(axis=1) / (r.std(axis=1, ddof=1) / np.sqrt(n))
mejor = float(t.max())

print(f"mejor t de {m} estrategias sin alpha: {mejor:.2f}")      # -> 3.14
print(f"p-valor sin ajustar: {2 * (1 - Z.cdf(mejor)):.5f}")      # -> 0.00169
print(f"t esperado del maximo por azar: {np.sqrt(2 * np.log(m)):.2f}")   # -> 3.72
print(f"t exigido por Bonferroni: {Z.inv_cdf(1 - 0.025 / m):.2f}")       # -> 4.06
