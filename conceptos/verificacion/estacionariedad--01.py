import numpy as np

# Serie trimestral con tendencia clara: cada trimestre sube ~2,5 de media
serie = np.array([20, 23, 25, 28, 30, 33, 35, 38, 40, 43, 45, 48])

primera, segunda = serie[:6], serie[6:]
print(f"media 1a mitad {primera.mean():.2f}   media 2a mitad {segunda.mean():.2f}")  # -> 26.50 y 41.50
print(f"varianza 1a    {primera.var(ddof=1):.2f}   varianza 2a    {segunda.var(ddof=1):.2f}")  # -> 22.70 y 22.70

# La primera diferencia quita la tendencia: ahora la media es estable
dif = np.diff(serie)
print(f"diferencias     {dif}")                    # -> [3 2 3 2 3 2 3 2 3 2 3]
print(f"media dif       {dif.mean():.2f}   varianza dif   {dif.var(ddof=1):.2f}")  # -> 2.55 y 0.27
