import numpy as np

rng = np.random.default_rng(2)
x = rng.normal(0, 1, size=60)
y = 0.5 * x + rng.normal(0, 1, size=60)
xc, yc = x - x.mean(), y - y.mean()

# El MLE de la pendiente coincide con el minimo cuadratico
pendiente = (xc @ yc) / (xc @ xc)
print(f"pendiente MLE/OLS {pendiente:.4f}")   # -> 0.3385
print(f"polyfit           {np.polyfit(x, y, 1)[0]:.4f}")  # -> 0.3385

# Con ruido normal, la log-verosimilitud depende solo del ECM de los residuos
residuos = yc - pendiente * xc
print(f"ECM               {(residuos ** 2).mean():.4f}")  # -> 0.9130

# El MLE de sigma^2 divide por n; el insesgado de Bessel por n-2
print(f"MLE de sigma^2    {(residuos ** 2).mean():.4f}")   # -> 0.9130
print(f"insesgado         {(residuos ** 2).sum() / (x.size - 2):.4f}")  # -> 0.9445
