"""metricas-de-clustering-1.py — cómo se lee un gráfico de silueta: el mismo dato agrupado con
el número de grupos correcto y con demasiados grupos. Cada barra es un punto."""

import numpy as np

from comun import *

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

estilo()

# Tres grupos compactos y separados: la respuesta es k = 3.
X, _ = make_blobs(n_samples=75, centers=[(0, 0), (6, 0), (0, 6)], cluster_std=1.0, random_state=3)
colores = [AZUL, ROJO, VERDE, NARANJA, MORADO, CIAN]

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3), sharex=True, sharey=True)

# Las dos notas van en la franja de arriba del panel: ocupan del 89 % del alto hacia arriba y
# la barra mas alta se queda en el 84 %. Para que no les cruce ninguna linea (con la rejilla
# entera, la linea del cero y las de 0,2 y 0,4 les pasaban por encima del texto), la rejilla
# vertical y las dos lineas de referencia se cortan a esta altura.
TOPE_NOTA = 0.88

for eje, k, nota in (
    (ejes[0], 3, "ninguna barra cruza el cero: cada punto\nencaja mejor en su grupo que en el vecino"),
    (ejes[1], 6, "partir en seis lo que son tres deja dos\nbarras a la izquierda del cero"),
):
    et = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
    s = metrics.silhouette_samples(X, et)
    fila = 0
    for g in range(k):
        idx = np.where(et == g)[0]
        idx = idx[np.argsort(s[idx])]          # dentro de cada grupo, de peor a mejor encaje
        eje.barh(np.arange(fila, fila + len(idx)), s[idx], height=1.0,
                 color=colores[g % len(colores)])
        fila += len(idx) + 4
    eje.axvline(0, color=REJILLA, linewidth=0.8, ymax=TOPE_NOTA)
    eje.axvline(s.mean(), color=TEXTO, linewidth=1.2, linestyle="--", ymax=TOPE_NOTA)
    eje.set_xlim(-0.4, 1.0)
    eje.set_ylim(0, 112)
    titulo(eje, ("k = %d: silueta media %.3f" % (k, s.mean())).replace(".", ","))
    eje.set_xlabel("coeficiente de silueta")
    eje.set_yticks([])
    anotar(eje, nota, (0, 0), (0.04, 0.93), flecha=False)
    rejilla(eje, eje="x")
    for linea in eje.xaxis.get_gridlines():    # la rejilla vertical, a la misma altura
        linea.set_ydata([0, TOPE_NOTA])
    numeros(eje, ejes="x")

ejes[0].set_ylabel("puntos, agrupados por cluster")

guardar(fig, "metricas-de-clustering-silueta")
