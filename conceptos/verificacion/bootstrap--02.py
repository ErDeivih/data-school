import numpy as np

rng = np.random.default_rng(3)
n = 40
x = rng.normal(0, 1, size=n)
y = 0.3 * x + rng.normal(0, 1, size=n)
xc, yc = x - x.mean(), y - y.mean()
pendiente = (xc @ yc) / (xc @ xc)
print(f"pendiente observada {pendiente:.3f}")   # -> 0.305

# Remuestreamos pares (x, y) y recalculamos la pendiente en cada remuestra
pendientes = np.empty(4000)
for i in range(4000):
    idx = rng.integers(0, n, size=n)
    a, b = xc[idx], yc[idx]
    pendientes[i] = (a @ b) / (a @ a)

print(f"error tipico bootstrap {pendientes.std(ddof=1):.3f}")   # -> 0.155
print(f"IC 95 %  [{np.percentile(pendientes, 2.5):.3f}, {np.percentile(pendientes, 97.5):.3f}]")  # -> [-0.003, 0.603]
