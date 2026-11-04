import io

import pandas as pd

# 20.000 importes: 19.000 con valor 10 y 1.000 con valor 100
valores = [10.0] * 19_000 + [100.0] * 1_000
texto = "importe\n" + "\n".join(str(v) for v in valores)

# En cada bloque se guardan la suma y la cuenta, no las filas
suma, cuenta, medias = 0.0, 0, []
for bloque in pd.read_csv(io.StringIO(texto), chunksize=7_500):
    suma += float(bloque["importe"].sum())
    cuenta += len(bloque)
    medias.append(float(bloque["importe"].mean()))

print(medias)                                # -> [10.0, 10.0, 28.0]
print(suma, cuenta, suma / cuenta)           # -> 290000.0 20000 14.5
print(round(sum(medias) / len(medias), 1))   # -> 16.0  la media de medias no es la media
