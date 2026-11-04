import numpy as np

def softmax(z, axis=-1):
    e = np.exp(z - z.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

rng = np.random.default_rng(0)
n, d_model = 4, 6
X = rng.normal(0, 1, (n, d_model))
# Esto es un GENERADOR, no una lista: el desempaquetado lo recorre tres veces y se agota.
Wq, Wk, Wv = (rng.normal(0, 0.5, (d_model, d_model)) for _ in range(3))
Q, K, V = X @ Wq, X @ Wk, X @ Wv

# Mascara causal: -infinito por encima de la diagonal, antes del softmax.
# k=1 salta la diagonal principal: cada token SI puede mirarse a si mismo.
causal = np.triu(np.full((n, n), -np.inf), k=1)
# Aqui d_model hace de d_k porque las proyecciones son cuadradas; con varias cabezas el
# divisor seria d_k = d_model / h.
pesos = softmax(Q @ K.T / np.sqrt(d_model) + causal)
print(pesos.round(3).tolist())
# -> [[1.0, 0.0, 0.0, 0.0], [0.475, 0.525, 0.0, 0.0],
#     [0.198, 0.369, 0.433, 0.0], [0.217, 0.299, 0.347, 0.136]]
# Si cada fila suma 1, la mascara se aplico antes del softmax y no lo descompenso.
print("cada fila suma:", pesos.sum(axis=1).round(3).tolist())   # -> [1.0, 1.0, 1.0, 1.0]
