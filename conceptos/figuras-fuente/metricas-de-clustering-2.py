"""metricas-de-clustering-2.py — el caso en que la silueta se equivoca: dos formas alargadas
que se enganchan. La silueta prefiere el corte de K-means; la validez por densidad, no."""

import numpy as np

from comun import *

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import make_moons

estilo()


def mst(matriz):
    """Árbol de recubrimiento mínimo, simetrizado (scipy lo guarda en un triángulo)."""
    from scipy.sparse.csgraph import minimum_spanning_tree

    m = minimum_spanning_tree(matriz).toarray()
    return np.maximum(m, m.T)


def dbcv(X, et, k=5):
    """Validez por densidad: 1 = grupos densos y bien separados, negativo = mal separados."""
    from scipy.spatial.distance import pdist, squareform

    D = squareform(pdist(X))
    nucleo = np.sort(D, axis=1)[:, min(k, len(X) - 1)]
    mrd = np.maximum(D, np.maximum(nucleo[:, None], nucleo[None, :]))
    np.fill_diagonal(mrd, 0.0)
    grupos = np.unique(et)
    dsc = {g: mst(mrd[np.ix_(et == g, et == g)]).max() for g in grupos}
    dspc = {}
    for g in grupos:
        cortes = []
        for h in grupos:
            if h == g:
                continue
            idx = np.r_[np.where(et == g)[0], np.where(et == h)[0]]
            cruce = mst(mrd[np.ix_(idx, idx)])[: np.sum(et == g), np.sum(et == g):]
            cortes.append(cruce[cruce > 0].min())
        dspc[g] = min(cortes) if cortes else np.inf
    val = [(dspc[g] - dsc[g]) / max(dspc[g], dsc[g]) for g in grupos]
    return float(np.average(val, weights=[np.sum(et == g) for g in grupos]))


X, verdad = make_moons(n_samples=400, noise=0.06, random_state=0)
kmeans = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(X)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3), sharex=True, sharey=True)

for eje, et, titulo_panel, nota in (
    (ejes[0], verdad, "Los dos grupos reales",
     "esta es la partición correcta\nsilueta 0,330\nDBCV 0,330"),
    (ejes[1], kmeans, "Lo que corta K-means con k = 2",
     "esta partición es incorrecta\nsilueta 0,489\nDBCV -0,789"),
):
    for g, color_g in ((0, AZUL), (1, MORADO)):
        eje.scatter(X[et == g, 0], X[et == g, 1], s=9, color=color_g, linewidths=0)
    eje.set_title(titulo_panel)
    eje.set_xlabel("variable 1")
    eje.set_ylim(-0.95, 1.25)
    anotar(eje, nota, (0, 0), (0.03, 0.10), flecha=False, fondo=True)
    rejilla(eje)
    numeros(eje)
ejes[0].set_ylabel("variable 2")

guardar(fig, "metricas-de-clustering-densidad")
