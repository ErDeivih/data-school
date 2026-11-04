import numpy as np
from math import gamma, pi

# Lado del cubo necesario para cubrir el 10 % del volumen de un cubo unidad
for d in (1, 2, 3, 5, 10, 50, 100, 1000):
    print("d=%4d  lado para el 10 %% del volumen: %.4f" % (d, 0.1 ** (1 / d)))
# -> d=   1  lado para el 10 % del volumen: 0.1000
# -> d=  10  lado para el 10 % del volumen: 0.7943
# -> d=1000  lado para el 10 % del volumen: 0.9977

# Fraccion del cubo que ocupa la esfera inscrita: pi^(d/2) / (2^d * Gamma(d/2+1))
for d in (2, 3, 10, 100):
    print("d=%3d  esfera inscrita / cubo: %.3e" % (d, pi ** (d / 2) / (2 ** d * gamma(d / 2 + 1))))
# -> d=  2  esfera inscrita / cubo: 7.854e-01
# -> d= 10  esfera inscrita / cubo: 2.490e-03
# -> d=100  esfera inscrita / cubo: 1.868e-70
