import numpy as np

# f(x) = 3x^2 + 6x + 11 es convexa: todo punto que anula la derivada es el mínimo global.
f = lambda x: 3 * x**2 + 6 * x + 11
df = lambda x: 6 * x + 6

# Comprobación de la desigualdad de la cuerda en muchos pares de puntos
rng = np.random.default_rng(0)
x = rng.uniform(-5, 5, size=200)
y = rng.uniform(-5, 5, size=200)
theta = rng.uniform(0, 1, size=200)
cuerda = f(theta * x + (1 - theta) * y) - (theta * f(x) + (1 - theta) * f(y))

print("se cumple la desigualdad de la cuerda:", bool(cuerda.max() <= 1e-6))   # salida: True
print("minimo de la funcion                 :", round(float(f(-1.0)), 4))    # salida: 8.0
print("derivada en x=-1                     :", round(float(df(-1.0)), 8))   # salida: 0.0
