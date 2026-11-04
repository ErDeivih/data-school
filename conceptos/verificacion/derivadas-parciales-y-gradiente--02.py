import numpy as np

# El gradiente no es una dirección universal: cambia de punto en punto.
f = lambda x, y: x**2 + 2 * x * y + 3 * y**2

def grad_numerico(x, y, h=1e-6):
    fx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    fy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    return round(fx, 4), round(fy, 4)

for punto in [(1.0, 2.0), (0.0, 0.0), (-2.0, 1.0)]:
    print("punto", punto, "gradiente", grad_numerico(*punto))
# salida:
# punto (1.0, 2.0) gradiente (6.0, 14.0)
# punto (0.0, 0.0) gradiente (0.0, 0.0)
# punto (-2.0, 1.0) gradiente (-2.0, 2.0)
