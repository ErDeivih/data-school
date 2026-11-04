import numpy as np

rng = np.random.default_rng(7)
n = 400
t = np.arange(n, dtype=float)
y = 0.5 * t + rng.normal(0, 2.0, n)
idx = np.arange(n)

def walk_forward(ventana=None):
    """Error por bloque con ventana expansiva, o movil si se fija el tamano."""
    errores = []
    for bloque in np.array_split(idx, 5)[1:]:
        entrena = idx[idx < bloque[0]]
        if ventana:
            entrena = entrena[-ventana:]
        coef = np.polyfit(t[entrena], y[entrena], 1)   # minimos cuadrados con numpy
        pred = np.polyval(coef, t[bloque])
        errores.append(float(np.sqrt(np.mean((y[bloque] - pred) ** 2))))
    return np.array(errores)

expansiva, movil = walk_forward(), walk_forward(60)
print("expansiva  media %.2f  bloques %s"
      % (expansiva.mean(), " ".join("%.2f" % e for e in expansiva)))
# -> expansiva  media 1.96  bloques 2.13 1.87 1.92 1.90
print("movil 60   media %.2f  bloques %s"
      % (movil.mean(), " ".join("%.2f" % e for e in movil)))
# -> movil 60   media 2.28  bloques 2.63 1.93 2.65 1.90
print("naive del ultimo valor %.2f" % np.sqrt(np.mean((y[1:] - y[:-1]) ** 2)))
# -> naive del ultimo valor 2.63
