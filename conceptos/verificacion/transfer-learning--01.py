import numpy as np


def entrena(X, y, epocas, params=None, semilla=0):
    """Red 2-8-1 con ReLU y entropia cruzada, por lotes. Devuelve W1, b1, w2, b2."""
    rng = np.random.default_rng(semilla)
    if params is None:
        W1, b1 = rng.normal(0, 0.7, (2, 8)), np.zeros(8)
        w2, b2 = rng.normal(0, 0.35, 8), 0.0
    else:
        # .copy() en las matrices y los vectores: sin el, el descenso de gradiente escribe
        # sobre los pesos del modelo de origen y la segunda llamada empezaria de otro sitio.
        W1, b1, w2, b2 = params[0].copy(), params[1].copy(), params[2].copy(), params[3]

    for _ in range(epocas):
        orden = rng.permutation(len(y))          # barajar una vez por epoca, no por lote
        for inicio in range(0, len(y), 32):
            idx = orden[inicio:inicio + 32]
            H = np.maximum(0.0, X[idx] @ W1 + b1)
            # [:, None] convierte el error en columna (lote, 1): asi el broadcasting alinea
            # las filas de H con las filas del error en vez de con las columnas.
            dz = (1 / (1 + np.exp(-(H @ w2 + b2))) - y[idx])[:, None] / len(idx)
            g = dz * w2 * (H > 0)                 # (H > 0) es la derivada de ReLU
            W1 -= 0.05 * (X[idx].T @ g)
            b1 -= 0.05 * g.sum(0)
            w2 -= 0.05 * (H * dz).sum(0)
            b2 -= 0.05 * float(dz.sum())
    return W1, b1, w2, b2


def precision(X, y, params):
    W1, b1, w2, b2 = params
    p = 1 / (1 + np.exp(-(np.maximum(0.0, X @ W1 + b1) @ w2 + b2)))
    return float(((p > 0.5) == y).mean())


def datos(rng, n, centro, escala):
    X = rng.normal(centro, escala, size=(n, 2))
    return X, (X[:, 0] * X[:, 1] > 0).astype(float)   # regla XOR: no hay recta que la separe


X_origen, y_origen = datos(np.random.default_rng(0), 400, 0.0, 1.0)
X_destino, y_destino = datos(np.random.default_rng(2), 12, 0.4, 0.7)   # solo 12 etiquetas
X_test, y_test = datos(np.random.default_rng(1), 400, 0.4, 0.7)

origen = entrena(X_origen, y_origen, 200)
desde_cero = entrena(X_destino, y_destino, 200)
transferido = entrena(X_destino, y_destino, 200, params=origen)

print(f"red de origen en su propia tarea   {precision(X_origen, y_origen, origen):.3f}")
print(f"desde cero con 12 etiquetas        {precision(X_test, y_test, desde_cero):.3f}")
print(f"partiendo del modelo de origen     {precision(X_test, y_test, transferido):.3f}")
# -> red de origen en su propia tarea   0.975
# -> desde cero con 12 etiquetas        0.657
# -> partiendo del modelo de origen     0.910
