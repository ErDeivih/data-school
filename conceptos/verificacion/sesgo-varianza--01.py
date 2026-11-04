import numpy as np

def f(x):
    return np.sin(2 * np.pi * x)

rng = np.random.default_rng(1)
x = np.linspace(0, 1, 30)
sigma, replicas = 0.3, 300
grados = [0, 1, 2, 3, 4, 5, 6, 7, 9]

# 300 muestras distintas por grado: asi se ve la variabilidad del propio ajuste
pred = {g: np.zeros((replicas, x.size)) for g in grados}
for r in range(replicas):
    y = f(x) + rng.normal(0, sigma, x.size)
    for g in grados:
        pred[g][r] = np.polyval(np.polyfit(x, y, g), x)

print("grado  sesgo^2  varianza  error")
for g in grados:
    media = pred[g].mean(axis=0)
    sesgo2 = np.mean((media - f(x)) ** 2)
    var = np.mean(pred[g].var(axis=0))
    print("%5d  %7.4f  %8.4f  %7.4f" % (g, sesgo2, var, sesgo2 + var))
# ->     3   0.0056    0.0120   0.0176
# ->     9   0.0002    0.0296   0.0298
print("varianza irreducible %.4f" % sigma ** 2)      # -> varianza irreducible 0.0900
