import numpy as np

# Muestreo ponderado por transformada inversa: las sumas acumuladas reparten [0, 1).
pesos = np.array([0.5, 0.3, 0.2])
acumulada = np.cumsum(pesos)                # [0.5, 0.8, 1.0]

rng = np.random.default_rng(0)              # semilla fija: el resultado se repite igual
sorteos = rng.random(10_000)
elegido = np.searchsorted(acumulada, sorteos)

print("frecuencias observadas:", np.round(np.bincount(elegido, minlength=3) / sorteos.size, 3))
print("frecuencias esperadas: ", pesos)
# la salida es, respectivamente, [0.499 0.299 0.202] y [0.5 0.3 0.2]
