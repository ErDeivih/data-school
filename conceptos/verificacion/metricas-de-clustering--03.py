import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import pdist, squareform
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import make_moons

def mst(matriz):
    """Arbol de recubrimiento minimo, simetrizado (scipy lo guarda en un triangulo)."""
    m = minimum_spanning_tree(matriz).toarray()
    return np.maximum(m, m.T)

def dbcv(X, et, k=5):
    """Validez por densidad (Moulavi et al., 2014): 1 = grupos densos y separados."""
    D = squareform(pdist(X))
    nucleo = np.sort(D, axis=1)[:, min(k, len(X) - 1)]        # al vecino k-esimo
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
            cruce = mst(mrd[np.ix_(idx, idx)])[:np.sum(et == g), np.sum(et == g):]
            cortes.append(cruce[cruce > 0].min())            # solo aristas que existen
        dspc[g] = min(cortes) if cortes else np.inf
    val = [(dspc[g] - dsc[g]) / max(dspc[g], dsc[g]) for g in grupos]
    return float(np.average(val, weights=[np.sum(et == g) for g in grupos]))

X4 = np.array([[0.0, 0.0], [0.0, 2.0], [10.0, 0.0], [10.0, 2.0]])
print("rectangulo por x:", round(dbcv(X4, np.array([0, 0, 1, 1]), k=1), 3))   # -> 0.8
print("rectangulo por y:", round(dbcv(X4, np.array([0, 1, 0, 1]), k=1), 3))   # -> -0.8

X, verdad = make_moons(n_samples=400, noise=0.06, random_state=0)
kmeans = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(X)
print("lunas de verdad  silueta %.3f  dbcv %.3f"
      % (metrics.silhouette_score(X, verdad), dbcv(X, verdad)))
# -> lunas de verdad  silueta 0.330  dbcv 0.330
print("lunas por k-means silueta %.3f  dbcv %.3f"
      % (metrics.silhouette_score(X, kmeans), dbcv(X, kmeans)))
# -> lunas por k-means silueta 0.489  dbcv -0.789
