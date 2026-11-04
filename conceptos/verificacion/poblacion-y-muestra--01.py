import numpy as np
from itertools import combinations

# Los seis sueldos que forman la poblacion completa (N = 6)
poblacion = np.array([1200, 1500, 1800, 2100, 2400, 3000])
print(f"media poblacional: {poblacion.mean():.1f}")  # -> 2000.0

# Todas las muestras posibles de tamano 2: son 15
pares = np.array(list(combinations(poblacion, 2)))
medias = pares.mean(axis=1)
print(f"numero de muestras: {len(pares)}")       # -> 15
print(f"menor media muestral: {medias.min():.1f}")  # -> 1350.0
print(f"mayor media muestral: {medias.max():.1f}")  # -> 2700.0
print(f"media de las 15 medias: {medias.mean():.1f}")  # -> 2000.0
