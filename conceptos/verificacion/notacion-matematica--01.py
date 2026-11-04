import numpy as np

x = np.array([3.0, 5.0, 7.0, 9.0])

# Σ es un sumatorio y Π un productorio: en NumPy son dos funciones y nada más.
# Se imprimen los nombres en ASCII para que el ejemplo funcione en cualquier consola.
print("sumatorio  x_i =", x.sum())      # -> 24.0
print("producto   x_i =", x.prod())     # -> 945.0
print("media      x_i =", (1 / x.size) * x.sum())   # -> 6.0

# La derivada parcial ∂f/∂x, con una sola variable, se aproxima con diferencias
# finitas centradas.
f = lambda v: 3 * v**2 * 5          # f(x, 5) = 3x²·5
h = 1e-6
print("parcial en x=2 ~", round((f(2 + h) - f(2 - h)) / (2 * h), 1))   # -> 60.0
