import numpy as np

def acf(x, nlags):
    d = x - x.mean()
    g0 = (d @ d) / d.size
    return np.array([1.0] + [(d[k:] @ d[:-k]) / d.size / g0 for k in range(1, nlags + 1)])

def pacf(r, nlags):
    """Durbin-Levinson: la PACF es el ultimo coeficiente de cada AR(k)."""
    phi = np.zeros((nlags + 1, nlags + 1))
    phi[1, 1] = r[1]
    for k in range(2, nlags + 1):
        num = r[k] - phi[k - 1, 1:k] @ r[k - 1:0:-1]
        den = 1 - phi[k - 1, 1:k] @ r[1:k]
        phi[k, k] = num / den
        phi[k, 1:k] = phi[k - 1, 1:k] - phi[k, k] * phi[k - 1, k - 1:0:-1]
    return np.array([phi[k, k] for k in range(1, nlags + 1)])

rng = np.random.default_rng(1)
n = 600
y = np.zeros(n)
for t in range(1, n):                     # AR(1) con phi = 0.8
    y[t] = 0.8 * y[t - 1] + rng.normal(0, 1)
y = y[100:]                               # descartamos el arranque

r = acf(y, 3)
print("acf  retardos 1..3", np.round(r[1:], 3))       # -> [0.779 0.624 0.526]
print("pacf retardos 1..3", np.round(pacf(r, 3), 3))  # -> [0.779 0.043 0.069]
print("banda del 95%", round(1.96 / np.sqrt(y.size), 3))  # -> 0.088
