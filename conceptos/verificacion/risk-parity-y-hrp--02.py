import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform

vol = np.array([0.10, 0.12, 0.25, 0.28])
corr = np.array([[1.0, 0.7, 0.2, 0.1],
                 [0.7, 1.0, 0.2, 0.1],
                 [0.2, 0.2, 1.0, 0.8],
                 [0.1, 0.1, 0.8, 1.0]])
cov = np.outer(vol, vol) * corr

def varianza_grupo(indices):
    """Varianza de un grupo con pesos de inversa de varianza dentro del grupo."""
    sub = cov[np.ix_(indices, indices)]
    inv = 1 / np.diag(sub)
    w = inv / inv.sum()
    return float(w @ sub @ w)

def hrp(cov):
    n = cov.shape[0]
    desv = np.sqrt(np.diag(cov))
    correl = cov / np.outer(desv, desv)
    distancia = np.sqrt(np.clip(0.5 * (1 - correl), 0, None))   # d = sqrt((1-rho)/2)
    np.fill_diagonal(distancia, 0.0)
    Z = linkage(squareform(distancia, checks=False), method="single")
    orden = list(dendrogram(Z, no_plot=True)["leaves"])         # cuasi-diagonalizacion
    pesos = np.ones(n)
    grupos = [orden]
    while grupos:                                               # biseccion recursiva
        siguientes = []
        for grupo in grupos:
            if len(grupo) <= 1:
                continue
            mitad = len(grupo) // 2
            izq, der = grupo[:mitad], grupo[mitad:]
            v_izq, v_der = varianza_grupo(izq), varianza_grupo(der)
            alfa = 1 - v_izq / (v_izq + v_der)                  # menos riesgo, mas peso
            for i in izq:
                pesos[i] *= alfa
            for i in der:
                pesos[i] *= 1 - alfa
            siguientes += [izq, der]
        grupos = [g for g in siguientes if len(g) > 1]
    return orden, pesos / pesos.sum()

orden, pesos = hrp(cov)
print("orden de las hojas:", orden)                       # -> orden de las hojas: [2, 3, 0, 1]
print("pesos HRP:", np.round(pesos, 4).tolist())          # -> pesos HRP: [0.5089, 0.3534, 0.0766, 0.0611]
print("volatilidad HRP:", round(float(np.sqrt(pesos @ cov @ pesos)), 4))   # -> volatilidad HRP: 0.0981
print("volatilidad a partes iguales:", round(float(np.sqrt(np.full(4, 0.25) @ cov @ np.full(4, 0.25))), 4))   # -> volatilidad a partes iguales: 0.1433
