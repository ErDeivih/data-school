import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons

# Dos lunas entrelazadas: K-means tiene que cortarlas, DBSCAN las sigue enteras.
X, verdad = make_moons(n_samples=300, noise=0.06, random_state=0)

km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
print(f"k-means k=2  acuerdo con los grupos reales {max((km.labels_ == verdad).mean(), (km.labels_ != verdad).mean()):.3f}")

for eps in (0.1, 0.12, 0.3):
    d = DBSCAN(eps=eps, min_samples=5).fit(X)
    # Comparamos solo los puntos que DBSCAN asigna a algun grupo: el ruido no tiene etiqueta real.
    fuera_ruido = d.labels_ != -1
    acuerdo = max((d.labels_[fuera_ruido] == verdad[fuera_ruido]).mean(),
                  (d.labels_[fuera_ruido] != verdad[fuera_ruido]).mean())
    n_grupos = len(set(d.labels_[fuera_ruido])) if fuera_ruido.any() else 0
    print(f"DBSCAN eps={eps:<5} grupos {n_grupos}  ruido {int((~fuera_ruido).sum()):>3} de {len(X)}  "
          f"acuerdo {acuerdo:.3f}")
# -> k-means k=2  acuerdo con los grupos reales 0.743
# -> DBSCAN eps=0.1   grupos 11  ruido  15 de 300  acuerdo 0.937
# -> DBSCAN eps=0.12  grupos 2  ruido   5 de 300  acuerdo 1.000
# -> DBSCAN eps=0.3   grupos 1  ruido   0 de 300  acuerdo 0.500
