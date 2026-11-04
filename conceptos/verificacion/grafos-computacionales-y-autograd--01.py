import numpy as np

# El mismo grafo del ejemplo, con la pasada hacia atras escrita a mano.
def perdida(x, w, b):
    z = x * w + b
    return z ** 2, z                   # devuelve tambien z: la derivada local vale 2*z

x, w, b = 2.0, 3.0, 1.0
y, z = perdida(x, w, b)                # desempaqueta la tupla: y = z**2  y  z = z

dy_dz = 2 * z                       # derivada local de la ultima operacion
print(f"y          {y:.1f}")         # -> y          49.0
print(f"dy/dw      {dy_dz * x:.1f}")  # -> dy/dw      28.0
print(f"dy/db      {dy_dz:.1f}")     # -> dy/db      14.0
print(f"dy/dx      {dy_dz * w:.1f}")  # -> dy/dx      42.0

eps = 1e-6                          # diferencias finitas para comprobar
print(f"numerico    {(perdida(x, w + eps, b)[0] - y) / eps:.4f}")
# -> numerico    28.0000
