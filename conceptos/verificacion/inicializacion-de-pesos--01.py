import numpy as np

# Propagacion de la varianza en una red ReLU de 10 capas y 256 unidades. Cada capa
# multiplica la varianza por 0.5 * 256 * Var(w): el 0.5 es el ReLU, que apaga la mitad.
rng = np.random.default_rng(0)
ancho = 256
entrada = rng.normal(size=ancho)          # activaciones de partida, desviacion 1

inicializaciones = [("std 0.01", 0.01),
                    ("Xavier", np.sqrt(2 / (ancho + ancho))),
                    ("He", np.sqrt(2 / ancho))]

print("inicializacion   capa 1   capa 2   capa 5  capa 10")
for nombre, escala in inicializaciones:
    x = entrada.copy()
    fila = []
    for capa in range(10):
        # normal(media, desviacion, forma): la escala es la DESVIACION, no la varianza
        w = rng.normal(0, escala, size=(ancho, ancho))
        x = np.maximum(0.0, w @ x)        # capa lineal + ReLU
        if capa in (0, 1, 4, 9):
            fila.append(f"{x.std():.2e}")
    print(f"{nombre:<14} " + "  ".join(fila))
# -> inicializacion   capa 1   capa 2   capa 5  capa 10
# -> std 0.01       9.66e-02  1.02e-02  1.66e-05  3.18e-10
# -> Xavier         5.64e-01  3.86e-01  1.42e-01  2.20e-02
# -> He             7.78e-01  8.47e-01  6.39e-01  7.22e-01
