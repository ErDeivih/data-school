import numpy as np
import pandas as pd

# Cinco dias medidos cada 5 minutos: onda diaria suave y ruido de desviacion 0.8
azar = np.random.default_rng(0)
minutos = pd.date_range("2026-01-05", periods=5 * 24 * 12, freq="5min")
t = np.arange(len(minutos))
base = 50 + 6 * np.sin(2 * np.pi * t / 288) + azar.normal(0.0, 0.8, len(t))
sin_pico = pd.Series(base, index=minutos)
con_pico = sin_pico.copy()
con_pico.iloc[300:306] += 12.0        # media hora de sobrecalentamiento

for etiqueta, regla in [("5 min", "5min"), ("1 hora", "1h"), ("1 dia", "1D")]:
    a = sin_pico.resample(regla).mean()
    b = con_pico.resample(regla).mean()
    print("%-7s n=%5d  subida del pico=%6.2f  desviacion del nivel=%.2f"
          % (etiqueta, len(a), (b - a).abs().max(), a.std()))
# -> 5 min   n= 1440  subida del pico= 12.00  desviacion del nivel=4.29
# -> 1 hora  n=  120  subida del pico=  6.00  desviacion del nivel=4.22
# -> 1 dia   n=    5  subida del pico=  0.25  desviacion del nivel=0.05
print("la serie de 5 minutos tiene desviacion %.3f" % sin_pico.std())
# -> la serie de 5 minutos tiene desviacion 4.287
