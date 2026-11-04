import numpy as np

rng = np.random.default_rng(0)
n = 5000
y = rng.normal(50, 10, size=n)

# MCAR: falta por un fallo del sensor, independiente del valor
mcar = y[rng.random(n) > 0.30]

# MNAR: faltan sistematicamente los valores mas altos (los que mas ganan no contestan)
mnar = y[y < np.quantile(y, 0.70)]

print(f"media completa  {y.mean():.2f}")     # -> 49.95
print(f"media con MCAR  {mcar.mean():.2f}")  # -> 49.78
print(f"media con MNAR  {mnar.mean():.2f}")  # -> 44.96
