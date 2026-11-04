import numpy as np


def reservoir(flujo, k, rng):
    """Devuelve una muestra uniforme de k elementos viendo el flujo una sola vez."""
    muestra = []
    for i, elemento in enumerate(flujo, start=1):
        if i <= k:
            muestra.append(elemento)
        else:
            j = rng.integers(0, i)        # entero uniforme en [0, i)
            if j < k:
                muestra[j] = elemento     # k / i, nunca k / n
    return muestra


rng = np.random.default_rng(0)
k, n, repeticiones = 10, 500, 1000
veces = np.zeros(n, dtype=int)
for _ in range(repeticiones):
    for elemento in reservoir(range(n), k, rng):
        veces[elemento] += 1

frecuencia = veces / repeticiones
print("probabilidad esperada: {:.3f}".format(k / n))    # -> 0.020
print("minima observada: {:.3f}".format(frecuencia.min()))   # -> 0.008
print("maxima observada: {:.3f}".format(frecuencia.max()))   # -> 0.035
print("media observada:  {:.3f}".format(frecuencia.mean()))  # -> 0.020
