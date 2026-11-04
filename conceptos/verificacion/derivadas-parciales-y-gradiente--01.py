import numpy as np

# f(x, y) = x**2 + 2xy + 3y**2 -> gradiente (2x + 2y, 2x + 6y)
def f(p):
    x, y = p
    return x**2 + 2 * x * y + 3 * y**2

def grad(p):
    x, y = p
    return np.array([2 * x + 2 * y, 2 * x + 6 * y])

# Descenso de gradiente: caminar en dirección contraria al gradiente.
# Con lr = 0.1 y una función con número de condición ~5.8, hacen falta unos cientos de pasos
# para acercarse al mínimo: la convergencia depende de la curvatura, no solo de la dirección.
p, lr = np.array([4.0, -3.0]), 0.1
for _ in range(250):
    p = p - lr * grad(p)

print("gradiente en (1,2):", grad(np.array([1.0, 2.0])))   # -> [ 6. 14.]
print("norma             :", round(float(np.linalg.norm(grad([1.0, 2.0]))), 2))  # -> 15.23
print("mínimo encontrado :", np.round(p, 8), "f =", round(float(f(p)), 8))       # salida: [ 0. -0.] f = 0.0
