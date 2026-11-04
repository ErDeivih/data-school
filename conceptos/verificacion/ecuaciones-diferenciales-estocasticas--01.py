import numpy as np

# GBM: un camino con Euler-Maruyama y el mismo camino con la solucion exacta
rng = np.random.default_rng(3)
mu, sigma, s0, T, n = 0.05, 0.25, 100.0, 1.0, 1000
dt = T / n
z = rng.standard_normal(n)

s = s0
for paso in range(n):
    s = s + mu * s * dt + sigma * s * np.sqrt(dt) * z[paso]

exacto = s0 * np.exp((mu - 0.5 * sigma ** 2) * T + sigma * np.sqrt(dt) * z.sum())

print(f"euler {s:.4f}")                                   # -> euler 138.0540
print(f"exacto {exacto:.4f}")                             # -> exacto 138.1202
print(f"error {abs(s - exacto):.4f}")                     # -> error 0.0662
print(f"error relativo {abs(s - exacto) / exacto:.4%}")   # -> error relativo 0.0479%