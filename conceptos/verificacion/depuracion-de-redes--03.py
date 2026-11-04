import numpy as np

# Gradiente con un valor enorme: sin recorte, un paso de SGD destruye los pesos
g = np.array([120.0, -310.0, 45.0, 8.0])
umbral = 5.0
norma = np.linalg.norm(g)
g_recortado = g * min(1.0, umbral / norma)

print(f"norma original   {norma:8.2f}")                       # -> 335.54
print(f"norma recortada  {np.linalg.norm(g_recortado):8.2f}")  # -> 5.00

# Una perdida NaN se detecta antes de que contamine los pesos
perdidas = np.array([0.693, 0.512, np.nan, 0.301])
print("hay NaN en la perdida:", bool((~np.isfinite(perdidas)).any()))   # -> True
