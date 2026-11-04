import numpy as np

c, phi = 5.0, 0.5                     # media de largo plazo: c/(1-phi) = 10
ultimo = 13.0                         # ultima observacion de la serie
print("media de largo plazo", c / (1 - phi))          # -> 10.0
for h in range(1, 4):
    ultimo = c + phi * ultimo
    print(f"pronostico h={h}: {ultimo:.3f}")
# -> h=1: 11.500   h=2: 10.750   h=3: 10.375
