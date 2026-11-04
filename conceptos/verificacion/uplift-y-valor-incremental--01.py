import numpy as np

T = np.array([1, 1, 1, 1, 0, 0, 0, 0])     # tratado / control
Y = np.array([1, 0, 1, 0, 1, 0, 0, 0])     # convirtio / no convirtio
z = 2 * Y - 1                               # +1 si convirtio, -1 si no
J = T * Y + (1 - T) * (1 - Y)               # etiqueta con los controles invertidos

# Con los dos grupos del mismo tamano, el uplift es la mitad de la diferencia de sus medias de z
tau = 0.5 * (z[T == 1].mean() - z[T == 0].mean())

print(f"tasa tratados {Y[T == 1].mean():.2f}  tasa control {Y[T == 0].mean():.2f}")
print(f"diferencia directa  {Y[T == 1].mean() - Y[T == 0].mean():.2f}")   # -> 0.25
print(f"media de z          {np.round([z[T == 1].mean(), z[T == 0].mean()], 2)}")
print(f"uplift              {tau:.2f}")                                   # -> 0.25
print(f"J por subgrupo      {np.round([J[:2].mean(), J[2:].mean()], 2)}")  # -> [0.5  0.67]
print(f"uplift subgrupo frio {0.5 * (z[2:4].mean() - z[6:8].mean()):.2f}")  # -> 0.50
