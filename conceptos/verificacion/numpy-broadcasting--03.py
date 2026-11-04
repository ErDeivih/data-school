import numpy as np

X = np.ones((3, 4))
print(X.shape, np.ones(3).shape)   # -> (3, 4) (3,)

# Se alinea por la derecha: 4 contra 3 no encaja y NumPy avisa en vez de adivinar
try:
    X + np.ones(3)
    print("no falla")
except ValueError:
    print("ValueError: no se puede alinear (3,4) con (3,)")   # -> ValueError: no se puede alinear (3,4) con (3,)

# Anadir el eje que falta con newaxis es la forma de arreglarlo
print((X + np.ones(3)[:, None]).shape)   # -> (3, 4)
