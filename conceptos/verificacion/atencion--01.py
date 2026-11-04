import numpy as np

def softmax(z):
    # Restar el maximo no cambia el resultado y evita desbordar exp() con puntuaciones grandes.
    # axis=-1 y keepdims=True: el softmax va POR FILAS y la suma conserva la forma (n, 1)
    # para que la division se reparta bien fila a fila.
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)

Q = np.array([[1.0, 0.0]])                     # una consulta
K = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
V = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
d_k = Q.shape[-1]                              # la ultima dimension de Q es d_k, no n

puntos = Q @ K.T            # K.T es (d_k, m): el producto da (n, m), consultas x claves
print("puntuaciones   ", puntos.round(4).tolist())                  # -> [[1.0, 0.0, 1.0]]
print("sin escalar    ", softmax(puntos).round(4).tolist())         # -> [[0.4223, 0.1554, 0.4223]]
pesos = softmax(puntos / np.sqrt(d_k))
print("con escalado   ", pesos.round(4).tolist())                  # -> [[0.4011, 0.1978, 0.4011]]
print("salida         ", (pesos @ V).round(4).tolist())             # -> [[0.8022, 0.5989]]

# Y el caso que rompe el softmax: dimension grande, puntuaciones grandes.
print("d_k=64 crudo   ", softmax(np.array([[8.0, 0.0, -8.0]])).round(4).tolist())
# -> [[0.9997, 0.0003, 0.0]]
print("d_k=64 escalado", softmax(np.array([[8.0, 0.0, -8.0]]) / 8).round(4).tolist())
# -> [[0.6652, 0.2447, 0.09]]
