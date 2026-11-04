import numpy as np

meses = np.arange(24)
serie = 100 + 2.0 * meses + 10 * np.sin(2 * np.pi * meses / 12) + np.array([1.0, -1.0] * 12)

# Promediar 12 meses promedia un ciclo entero: la estacionalidad se cancela.
media_movil = np.convolve(serie, np.ones(12) / 12, mode="valid")

print(f"desviacion de la serie       {serie.std(ddof=1):.2f}")        # -> 13.16
print(f"desviacion de la media movil {media_movil.std(ddof=1):.2f}")  # -> 7.79
