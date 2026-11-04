import numpy as np

h = np.array([2.0, -1.0, 0.5, 3.0])
p = 0.5
rng = np.random.default_rng(7)

mascara = (rng.random(h.size) >= p).astype(float)
# >= p deja la mascara a 1 con probabilidad 1-p; astype(float) la convierte en 0.0 y 1.0
print(f"mascara {mascara}")                              # -> mascara [1. 1. 1. 0.]
print(f"salida  {np.round(h * mascara / (1 - p), 2)}")   # -> salida  [ 4. -2.  1.  0.]

# La esperanza se conserva aunque cada sorteo concreto la mueva.
medias = []
for _ in range(20000):
    m = (rng.random(h.size) >= p).astype(float)
    medias.append((h * m / (1 - p)).mean())
print(f"media teorica {h.mean():.4f}  media simulada {np.mean(medias):.4f}")
# -> media teorica 1.1250  media simulada 1.1227
