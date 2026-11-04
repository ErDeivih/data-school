import numpy as np

# Por que hay que mirar cuantos experimentos se probaron: si un paper prueba 20
# variantes y publica la mejor, el ganador puede salir de puro ruido.
rng = np.random.default_rng(0)
n, variantes = 30, 20
t = []
for _ in range(variantes):
    a = rng.normal(0.0, 1.0, n)
    b = rng.normal(0.0, 1.0, n)      # mismo proceso: no hay ninguna diferencia real
    t.append((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / n + b.var(ddof=1) / n))

print("t de la mejor de 20 variantes:", round(max(t), 2))   # -> 2.42
print("variantes con t > 2:", int(np.sum(np.abs(t) > 2)), "de", variantes)   # -> 4 de 20
