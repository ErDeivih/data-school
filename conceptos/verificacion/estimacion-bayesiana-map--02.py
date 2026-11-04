import numpy as np

# Regularizar con L2 es poner una prior normal centrada en cero: MAP = ridge.
# Centramos x e y para que la penalizacion solo toque a la pendiente.
x = np.array([1.0, 1.1, 2.0, 2.2, 3.0, 3.1, 4.0, 4.2])
y = np.array([2.1, 2.5, 3.2, 3.6, 4.1, 4.4, 5.2, 5.6])
xc, yc = x - x.mean(), y - y.mean()

pendiente_ols = (xc @ yc) / (xc @ xc)
print(f"pendiente OLS {pendiente_ols:.4f}")   # -> 1.0119

# MAP = argmin de la suma de cuadrados + lambda * pendiente^2
for lam in (0.0, 0.5, 1.0, 2.0, 10.0):
    pendiente_map = (xc @ yc) / (xc @ xc + lam)
    print(f"lambda = {lam:>4.1f}  pendiente {pendiente_map:.4f}")

# Equivalencia con el prior: lambda = sigma^2 / tau^2.
# Con un prior normal de desviacion tau = 0,5 y un ruido de sigma = 1:
sigma, tau = 1.0, 0.5
print(f"lambda equivalente {sigma ** 2 / tau ** 2:.1f}")   # -> 4.0
