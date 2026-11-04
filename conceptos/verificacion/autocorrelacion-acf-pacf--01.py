import numpy as np

def acf(x, nlags):
    """Autocorrelaciones muestrales con denominador 1/n (el estimador sesgado)."""
    d = x - x.mean()
    g0 = (d @ d) / d.size
    return np.array([1.0] + [(d[k:] @ d[:-k]) / d.size / g0 for k in range(1, nlags + 1)])

y = np.array([2.0, 4.0, 3.0, 5.0, 4.0, 6.0])
desv = y - y.mean()
print("media", y.mean(), " suma de cuadrados", (desv ** 2).sum())        # -> media 4.0 y 10.0
print("numerador del retardo 1", (desv[1:] * desv[:-1]).sum())          # -> -1.0
print("acf retardos 0..3", np.round(acf(y, 3), 3))                      # -> [ 1.  -0.1  0.4 -0.4]
print("banda del 95%", round(1.96 / np.sqrt(y.size), 2))                # -> 0.8
