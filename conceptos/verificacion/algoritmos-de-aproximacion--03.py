import itertools
import numpy as np

# Cobertura maxima: elegir k conjuntos para cubrir el maximo de elementos.
universo = {1, 2, 3, 4, 5, 6}
conjuntos = {"A": {1, 2, 3}, "B": {1, 4, 5}, "C": {2, 3, 6}}
k = 2

cubierto, elegidos = set(), []
for _ in range(k):
    mejor = max(conjuntos, key=lambda s: len(conjuntos[s] - cubierto))
    elegidos.append(mejor)
    cubierto |= conjuntos[mejor]

optimo = max(len(set().union(*[conjuntos[s] for s in combo]))
             for combo in itertools.combinations(conjuntos, k))

print("voraz:", elegidos, "cubre", len(cubierto))       # -> cubre 5
print("optimo con 2 conjuntos:", optimo)                # -> 6
print("cociente: {:.3f}".format(len(cubierto) / optimo))          # -> 0.833
print("cota 1 - 1/e: {:.3f}".format(1 - 1 / np.e))                # -> 0.632
