import numpy as np

# Entrenar embeddings de juguete: acercar los pares que coocurren y alejar los negativos.
pares = [(0, 1), (1, 0), (2, 3), (3, 2)]      # gato-perro y coche-moto
rng = np.random.default_rng(0)
d = 8
U = rng.normal(0, 0.1, (4, d))                # vectores de centro
V = rng.normal(0, 0.1, (4, d))                # vectores de contexto
sig = lambda x: 1 / (1 + np.exp(-x))

for _ in range(3000):
    for c, o in pares:
        negs = [j for j in range(4) if j != c]
        negativos = [(negs[int(rng.integers(0, len(negs)))], 0.0) for _ in range(2)]
        for obj, etiqueta in [(o, 1.0)] + negativos:
            g = sig(float(U[c] @ V[obj])) - etiqueta
            Uc = U[c].copy()                  # copia antes de tocar la fila: se usa dos veces
            U[c] -= 0.5 * g * V[obj]
            V[obj] -= 0.5 * g * Uc

cos = lambda a, b: float(U[a] @ U[b] / (np.linalg.norm(U[a]) * np.linalg.norm(U[b])))
print("gato-perro:", round(cos(0, 1), 3))    # -> 0.998
print("coche-moto:", round(cos(2, 3), 3))    # -> 0.95
print("gato-coche:", round(cos(0, 2), 3))    # -> -0.038
