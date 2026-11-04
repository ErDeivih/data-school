import numpy as np

# Tres usuarios que han puntuado tres articulos (A, B, C) del 1 al 5.
train = np.array([(5.0, 4, 1),
                  (4.0, 3, 2),
                  (2.0, 1, 4)])
normas = np.linalg.norm(train, axis=0, keepdims=True)    # (1, 3): una norma por columna
similitud = (train.T @ train) / (normas.T @ normas)      # coseno entre columnas (articulos)
print("similitud A-B:", round(similitud[0, 1], 3),
      "A-C:", round(similitud[0, 2], 3),
      "B-C:", round(similitud[1, 2], 3))
# -> similitud A-B: 0.994 A-C: 0.683 B-C: 0.599

# Un cuarto usuario puntua A con 5 y C con 2. Queremos predecirle B.
medias = train.mean(axis=0)                              # una media por articulo
pesos = np.array([similitud[0, 1], similitud[2, 1]])     # parecido de A y C con B
valores = np.array([5.0, 2.0])
print("prediccion sin centrar:", round(float((pesos * valores).sum() / pesos.sum()), 3))
# -> prediccion sin centrar: 3.872
centrado = valores - np.array([medias[0], medias[2]])    # cada articulo respecto a su media
print("prediccion centrada:", round(float(medias[1] + (pesos * centrado).sum() / pesos.sum()), 3))
# -> prediccion centrada: 3.373
