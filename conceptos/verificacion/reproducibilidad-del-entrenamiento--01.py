import numpy as np


def entrena(semilla, tirada_extra=False):
    rng = np.random.default_rng(semilla)
    w = rng.normal(0, 0.1, 3)
    if tirada_extra:
        rng.random()                       # una sola tirada de mas...
    return w + rng.normal(0, 0.05, 3)      # ...desplaza todo lo que viene despues


a = entrena(0)
b = entrena(0)
c = entrena(0, tirada_extra=True)

print("misma semilla, mismo codigo:  ", bool(np.allclose(a, b)))      # -> True
print("misma semilla, una tirada mas:", bool(np.allclose(a, c)))      # -> False
print(f"distancia entre los dos pesos: {np.linalg.norm(a - c):.4f}")  # -> 0.0725
