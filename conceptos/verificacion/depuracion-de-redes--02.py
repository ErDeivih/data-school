import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(0, 1, (8, 2))                    # 8 ejemplos, 2 variables
y = np.array([0, 1, 0, 1, 0, 1, 0, 1])          # etiquetas casi arbitrarias

W1 = rng.normal(0, 0.5, (2, 16)); b1 = np.zeros(16)
W2 = rng.normal(0, 0.5, (16, 2)); b2 = np.zeros(2)
idx = np.arange(X.shape[0])

def perdida():
    h = np.tanh(X @ W1 + b1)
    z = h @ W2 + b2
    p = np.exp(z - z.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
    return -np.log(p[idx, y]).mean(), h, p

historial = {}
for epoca in range(1, 601):
    L, h, p = perdida()
    if epoca in (1, 200, 600):
        historial[epoca] = L
    g2 = p.copy(); g2[idx, y] -= 1; g2 /= X.shape[0]     # gradiente de la entropia cruzada + softmax
    g1 = (g2 @ W2.T) * (1 - h ** 2)
    W2 -= 0.5 * h.T @ g2; b2 -= 0.5 * g2.sum(0)
    W1 -= 0.5 * X.T @ g1; b1 -= 0.5 * g1.sum(0)

# Si la red no puede memorizar 8 ejemplos, el fallo esta en el codigo, no en los datos
print(f"epoca   1  perdida {historial[1]:.4f}")     # -> 0.6347
print(f"epoca 200  perdida {historial[200]:.4f}")   # -> 0.0648
print(f"epoca 600  perdida {historial[600]:.4f}")   # -> 0.0088
