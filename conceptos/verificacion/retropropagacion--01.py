import numpy as np

# Red minima: 3 entradas -> 2 neuronas ocultas (sigmoide) -> 1 salida (sigmoide)
X = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]])
y = np.array([[0.0], [1.0], [1.0], [0.0]])
W1 = np.array([[0.4, -0.6], [-0.2, 0.8], [0.5, 0.1]])
b1 = np.array([0.1, -0.1])
W2 = np.array([[1.2], [-0.9]])
b2 = np.array([0.2])

def sigmoide(z):
    return 1.0 / (1.0 + np.exp(-z))

def perdida(W1, b1, W2, b2):
    a1 = sigmoide(X @ W1 + b1)          # @ es producto matricial: (4x3) @ (3x2) -> (4x2)
    yg = sigmoide(a1 @ W2 + b2)
    return float(np.mean((yg - y) ** 2))   # float() saca el escalar de numpy a Python

# Paso hacia delante guardando lo que la regla de la cadena necesita despues
a1 = sigmoide(X @ W1 + b1)
yg = sigmoide(a1 @ W2 + b2)

# Paso hacia atras: delta de la salida y delta de la capa oculta
# El 2 y el 1/len(y) salen de derivar la media del cuadrado; yg*(1-yg) es la derivada de la sigmoide
d_salida = 2 * (yg - y) / len(y) * yg * (1 - yg)
gW2 = a1.T @ d_salida                   # la activacion anterior TRANSPUESTA por el delta
d_oculta = (d_salida @ W2.T) * a1 * (1 - a1)     # (W2)^T reparte el error hacia atras
gW1 = X.T @ d_oculta

print("perdida inicial          ", round(perdida(W1, b1, W2, b2), 6))   # -> 0.251452
print("gradiente dW2            ", np.round(gW2.ravel(), 6))           # -> [0.022698 0.02383 ]
