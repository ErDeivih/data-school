import numpy as np
import matplotlib.pyplot as plt

# Dos campanas con la MISMA media y desviaciones muy distintas:
# el resumen numerico no basta, hay que mirar la forma.
a = np.array([98, 100, 99, 101, 102, 100])
b = np.array([40, 160, 55, 145, 60, 140])

print(f"media A {a.mean():.1f}  desv A {a.std(ddof=1):.1f}")   # ddof=1: muestra, no poblacion
print(f"media B {b.mean():.1f}  desv B {b.std(ddof=1):.1f}")
print("rango A:", a.max() - a.min(), " rango B:", b.max() - b.min())

assert a.mean() == b.mean()          # la media no distingue nada: el grafico si
