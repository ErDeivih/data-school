import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=60, centers=[(0, 0), (5, 0), (0, 5)], cluster_std=0.5, random_state=0)

def w_k(datos, k, arranques=1):
    """Dispersion interna agrupada: lo que K-means minimiza, sin el factor 2n."""
    et = KMeans(n_clusters=k, n_init=arranques, random_state=0).fit_predict(datos)
    return sum(((datos[et == g] - datos[et == g].mean(0)) ** 2).sum() / (2 * (et == g).sum())
               for g in range(k))

azar = np.random.default_rng(0)
minimo, maximo = X.min(0), X.max(0)          # la caja que ocupan los datos
ks = [1, 2, 3, 4, 5]
gap, s = {}, {}
for k in ks:
    real = np.log(w_k(X, k, 5))              # tus datos, con varios arranques
    ref = np.array([np.log(w_k(azar.uniform(minimo, maximo, X.shape), k)) for _ in range(10)])
    gap[k], s[k] = ref.mean() - real, ref.std(ddof=1) * np.sqrt(1 + 1 / len(ref))
    print(f"k={k}  logW {real:7.3f}  gap {gap[k]:6.3f}  s {s[k]:5.3f}")
# -> k=1  logW   1.746  gap -0.398  s 0.109
# -> k=2  logW   1.088  gap  0.455  s 0.141
# -> k=3  logW  -0.374  gap  1.763  s 0.129
# -> k=4  logW  -0.311  gap  1.549  s 0.131
# -> k=5  logW  -0.226  gap  1.468  s 0.079

# Regla de Tibshirani: el k mas pequeno que ya no mejora lo suficiente.
elegido = min(k for k in ks[:-1] if gap[k] >= gap[k + 1] - s[k + 1])
print("regla del gap: k =", elegido)              # -> regla del gap: k = 3
