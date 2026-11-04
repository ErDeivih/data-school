import numpy as np

# Una tabla de embeddings es una matriz V x d: cada fila es un objeto.
V, d = 50000, 300
# Los 4 son los bytes de un float32; /1e6 pasa a MB decimales y /1024 a KiB binarios.
print("tabla densa:", V * d * 4 / 1e6, "MB")          # -> 60.0 MB
print("one-hot por palabra:", V * 4 / 1024, "KiB")    # -> 195.3125 KiB
print("todas one-hot:", V * V * 4 / 1e9, "GB")        # -> 10.0 GB

# Consultar un embedding es multiplicar el one-hot por la tabla: devuelve la fila.
E = np.array([[0.9, 0.1, 0.0, 0.0],    # gato
              [0.8, 0.2, 0.1, 0.0],    # perro
              [0.0, 0.1, 0.9, 0.2],    # coche
              [0.1, 0.0, 0.8, 0.3]])   # moto
# El one-hot por la matriz devuelve una fila NUEVA; E[1] seria una vista sobre la tabla.
print("fila recuperada:", (np.array([0.0, 1.0, 0.0, 0.0]) @ E).tolist())
# -> [0.8, 0.2, 0.1, 0.0]

def cos(u, v):
    # Sin axis, np.linalg.norm devuelve la norma de todo el vector aplanado, no la de cada
    # fila: con matrices de varios vectores habria que pasar axis=-1.
    return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))

print("coseno one-hot:", cos(np.array([1.0, 0, 0, 0]), np.array([0.0, 1, 0, 0])))  # -> 0.0
print("coseno denso  :", round(cos(E[0], E[1]), 3))                               # -> 0.984
print("coseno ajeno  :", round(cos(E[0], E[2]), 3))                               # -> 0.012
