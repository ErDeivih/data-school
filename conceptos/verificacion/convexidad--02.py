import numpy as np

# La convexidad también se ve en la segunda derivada: positiva en todo el dominio.
f = lambda x: 3 * x**2 + 6 * x + 11
theta = np.random.default_rng(1).uniform(-5, 5, size=200)   # 200 puntos del dominio

h = 1e-3    # con h más pequeño, el error de redondeo de la diferencia se come el resultado
segunda = (f(theta + h) - 2 * f(theta) + f(theta - h)) / h**2

print("segunda derivada numerica:", round(float(segunda.mean()), 4))    # salida: 6.0
print("todas positivas          :", bool(np.all(segunda > 0)))          # salida: True
