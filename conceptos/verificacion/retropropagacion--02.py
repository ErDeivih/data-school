import numpy as np

# La misma red, ahora comprobando el gradiente por diferencias finitas
X = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]])
y = np.array([[0.0], [1.0], [1.0], [0.0]])
W1 = np.array([[0.4, -0.6], [-0.2, 0.8], [0.5, 0.1]])
b1 = np.array([0.1, -0.1])
W2 = np.array([[1.2], [-0.9]])
b2 = np.array([0.2])

def sigmoide(z):
    return 1.0 / (1.0 + np.exp(-z))

def perdida(W1, b1, W2, b2):
    a1 = sigmoide(X @ W1 + b1)
    return float(np.mean((sigmoide(a1 @ W2 + b2) - y) ** 2))

a1 = sigmoide(X @ W1 + b1)
yg = sigmoide(a1 @ W2 + b2)
d_salida = 2 * (yg - y) / len(y) * yg * (1 - yg)
gW2 = a1.T @ d_salida

# Perturbamos cada peso de W2 y comparamos con el gradiente analitico
eps = 1e-6
num = np.zeros_like(W2)                 # misma forma y tipo que W2, rellena de ceros
for i in range(W2.shape[0]):
    W2p, W2m = W2.copy(), W2.copy()     # sin copy() las dos variables serian el mismo array
    W2p[i, 0] += eps
    W2m[i, 0] -= eps
    # Diferencia central: (f(x+h) - f(x-h)) / 2h, mas precisa que la hacia un solo lado
    num[i, 0] = (perdida(W1, b1, W2p, b2) - perdida(W1, b1, W2m, b2)) / (2 * eps)
print("diferencias finitas dW2  ", np.round(num.ravel(), 6))   # -> [0.022698 0.02383 ]

# Un paso de descenso de gradiente con tasa 0,5
print("perdida tras un paso     ", round(perdida(W1, b1, W2 - 0.5 * gW2, b2), 6))   # -> 0.25092
