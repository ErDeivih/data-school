import numpy as np

# La media minimiza la suma de cuadrados; la mediana, la suma de valores absolutos.
datos = np.array([1800.0, 1900, 2000, 2100, 2200, 2400, 9000])
candidatos = np.linspace(1500, 3500, 2001)

cuadrados = [((datos - c) ** 2).sum() for c in candidatos]
absolutos = [np.abs(datos - c).sum() for c in candidatos]

print("minimiza cuadrados:", round(candidatos[int(np.argmin(cuadrados))]))   # -> 3057  (la media)
print("minimiza absolutos:", round(candidatos[int(np.argmin(absolutos))]))   # -> 2100  (la mediana)
