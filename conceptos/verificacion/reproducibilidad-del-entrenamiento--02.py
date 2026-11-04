import numpy as np

# Cuatro ejecuciones del mismo codigo con la misma configuracion: solo cambia la semilla
acc = np.array([0.8450, 0.8312, 0.8503, 0.8388])
k = acc.size
media, s = acc.mean(), acc.std(ddof=1)
margen = 2 * s * np.sqrt(1 + 1 / k)          # intervalo de prediccion para UNA ejecucion nueva

print(f"media de las {k} ejecuciones  {media:.4f}")                      # -> 0.8413
print(f"dispersion entre semillas    {s:.4f}")                          # -> 0.0082
print(f"la proxima caera entre       {media - margen:.4f} y {media + margen:.4f}")   # -> 0.8229 y 0.8597
print(f"amplitud del intervalo       {2 * margen:.4f}")                 # -> 0.0368
