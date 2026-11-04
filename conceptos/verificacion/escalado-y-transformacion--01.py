import numpy as np

# Cinco valores normales y uno extremo: el mismo dato, dos escalados.
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 100.0])

minmax = (x - x.min()) / (x.max() - x.min())
z = (x - x.mean()) / x.std(ddof=1)      # ddof=1: estimamos la media de la muestra

print(f"min-max de 2.0   {minmax[1]:.4f}")   # -> 0.0101
print(f"min-max de 4.0   {minmax[3]:.4f}")   # -> 0.0303
print(f"z-score de 2.0   {z[1]:+.2f}")       # -> -0.43
print(f"z-score de 100   {z[5]:+.2f}")       # -> +2.04
