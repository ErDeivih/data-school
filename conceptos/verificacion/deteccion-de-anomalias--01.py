import numpy as np

consumo = np.array([10.0, 11, 12, 12, 13, 13, 14, 15, 100])   # el ultimo es el raro

# Version clasica: media y desviacion. El propio outlier las infla y se esconde.
z = (consumo - consumo.mean()) / consumo.std(ddof=1)   # ddof=1: divide entre n-1
print("media:", round(consumo.mean(), 2), "desviacion:", round(consumo.std(ddof=1), 2))
# -> media: 22.22 desviacion: 29.21
print("z-score del 100:", round(z[-1], 2))        # -> 2.66

# Version robusta: mediana y desviacion absoluta mediana (MAD).
mediana = np.median(consumo)
mad = np.median(np.abs(consumo - mediana))        # MAD: distancias a la mediana, y su mediana
z_mod = 0.6745 * (consumo - mediana) / mad        # 0,6745 deja las dos escalas comparables
print("mediana:", mediana, "MAD:", mad)           # -> mediana: 13.0 MAD: 1.0
print("z modificado del 100:", round(z_mod[-1], 2))   # -> 58.68
print("z modificado del 15:", round(z_mod[-2], 2))    # -> 1.35
