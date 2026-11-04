"""bases-de-datos-vectoriales-1.py — por qué el IVF pierde vecinos en la frontera y cuanto
recall se compra subiendo nprobe. Base de juguete de 600 vectores en 32 dimensiones agrupada
en 8 grupos con k-means. Figura de la pagina de bases de datos vectoriales (fase 8)."""

import numpy as np

from comun import *

estilo()

rng = np.random.default_rng(0)
centros = rng.normal(0, 1, size=(8, 32))
# Ruido alto a proposito: los grupos se solapan y la frontera del IVF se nota.
base = np.vstack([c + rng.normal(0, 2.0, size=(75, 32)) for c in centros])
base /= np.linalg.norm(base, axis=1, keepdims=True)
origen = np.repeat(np.arange(8), 75)


def dist2(X, Y):
    return (X ** 2).sum(1)[:, None] + (Y ** 2).sum(1)[None, :] - 2 * X @ Y.T


def kmeans(X, k, semilla=0, iteraciones=50):
    r = np.random.default_rng(semilla)
    C = X[r.choice(len(X), k, replace=False)].copy()
    for _ in range(iteraciones):
        etiquetas = np.argmin(dist2(X, C), axis=1)
        C = np.array([X[etiquetas == j].mean(0) if np.any(etiquetas == j) else C[j]
                      for j in range(k)])
    return C


C = kmeans(base, 8)
asignacion = np.argmin(dist2(base, C), axis=1)


def exactos(q, k=10):
    return set(np.argsort(dist2(q[None, :], base)[0])[:k])


# Recall medido para cada nprobe: es la curva que se compra con tiempo de consulta.
nprobes = np.arange(1, 9)
recalls = []
for nprobe in nprobes:
    aciertos = 0.0
    for q in base[rng.choice(len(base), 30, replace=False)] + rng.normal(0, 0.1, (30, 32)):
        cercanos = np.argsort(dist2(q[None, :], C)[0])[:nprobe]
        cand = np.flatnonzero(np.isin(asignacion, cercanos))
        d = dist2(base[cand], q[None, :])[:, 0]
        aciertos += len(set(cand[np.argsort(d)[:10]]) & exactos(q, 10)) / 10
    recalls.append(aciertos / 30)
recalls = np.array(recalls)


def pca2(X):
    """Proyección a dos dimensiones con las dos direcciones de más varianza (SVD)."""
    Xc = X - X.mean(0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    return U[:, :2] * S[:2]


# Los puntos que el IVF pierde al visitar un solo grupo: su grupo asignado no es el unico
# candidato razonable, asi que una consulta puede mirar en el grupo de al lado.
margen = np.sort(dist2(base, C), axis=1)
frontera = margen[:, 1] < 1.2 * margen[:, 0]

# Tres paneles en una fila dejaban cada uno demasiado estrecho y los textos acababan
# pisandose: van en dos filas, y el del recall se queda con la de abajo entera.
fig = plt.figure(figsize=(9.6, 7.6))
rejilla_paneles = fig.add_gridspec(2, 2)
p_grupos = fig.add_subplot(rejilla_paneles[0, 0])
p_frontera = fig.add_subplot(rejilla_paneles[0, 1])
p_recall = fig.add_subplot(rejilla_paneles[1, :])
# Se dibuja uno de cada dos puntos: con 600 marcas el SVG pasa de 200 KB y la nube no se
# lee mejor. La forma de los grupos es la misma.
muestra = slice(None, None, 2)
# Panel 1: los 8 grupos con los que se generaron los datos. El color es el grupo de origen,
# y se ve que el ruido los solapa: la nube no viene troceada.
puntos = pca2(base)
mapa = plt.get_cmap("tab10")
for j in range(8):
    m = origen == j
    p_grupos.scatter(puntos[m, 0][muestra], puntos[m, 1][muestra], s=9, color=mapa(j),
                     alpha=0.85, linewidths=0)
titulo(p_grupos, "Ocho grupos con ruido", "la nube se solapa: no viene troceada")
rejilla(p_grupos, "both")
numeros(p_grupos)

# Panel 2: la misma nube, ahora con los grupos que decide k-means: el corte ya es una
# frontera entre centroides, y los puntos que caen cerca de ella son los que el IVF
# pierde cuando visita un solo grupo.
for j in range(8):
    m = asignacion == j
    p_frontera.scatter(puntos[m, 0][muestra], puntos[m, 1][muestra], s=9, color=AZUL,
                       alpha=0.6, linewidths=0)
p_frontera.scatter(puntos[frontera, 0], puntos[frontera, 1], s=22, facecolors="none",
                   edgecolors=ROJO, linewidths=0.9)
titulo(p_frontera, "El IVF corta por centroides",
       "los puntos de la frontera se pierden al visitar un solo grupo")
p_frontera.set_xlabel(f"los {int(frontera.sum())} puntos marcados están a menos de\n"
                      "un 20 % de dos grupos a la vez")
rejilla(p_frontera, "both")
numeros(p_frontera)

# Panel 3: el recall que se compra subiendo nprobe
p_recall.plot(nprobes, recalls, color=MORADO, linewidth=1.8, marker="o", markersize=4)
for nprobe in (1, 4):
    r = recalls[nprobe - 1]
    p_recall.plot([nprobe], [r], "o", color=ROJO, markersize=6)
    p_recall.annotate(f"{r:.2f}".replace(".", ","), (nprobe, r), textcoords="offset points",
                      xytext=(6, -12), color=ROJO, fontsize=9)
p_recall.set_ylim(0.5, 1.05)
p_recall.set_xticks(nprobes)
titulo(p_recall, "Subir nprobe compra recall", "más grupos visitados: más recall y más tiempo")
p_recall.set_xlabel("nprobe (grupos visitados)")
p_recall.set_ylabel("recall@10")
rejilla(p_recall)
numeros(p_recall)

guardar(fig, "vectorial-frontera-y-recall")
