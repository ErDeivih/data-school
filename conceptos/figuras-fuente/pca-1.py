"""pca-1.py — de qué vive el análisis de componentes principales: unas pocas direcciones se
llevan casi toda la varianza y todas las demás se pueden tirar. Página de PCA (fase 6)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Izquierda: ocho variables que en realidad se mueven con tres factores ocultos.
factores = azar.normal(size=(400, 3))
cargas = azar.normal(size=(8, 3)) * np.array([1.0, 0.8, 0.5])
X = factores @ cargas.T + azar.normal(scale=0.4, size=(400, 8))
Xc = X - X.mean(axis=0)                       # PCA mide dispersión: hay que centrar antes
S = Xc.T @ Xc / (Xc.shape[0] - 1)             # covarianzas, dividiendo entre n-1
valores = np.linalg.eigvalsh(S)[::-1]         # autovalores de mayor a menor = varianza por eje
proporcion = valores / valores.sum()          # cuota de varianza de cada dirección
acumulada = np.cumsum(proporcion)
print("explicada:", np.round(proporcion, 3).tolist())
print("acumulada:", np.round(acumulada, 3).tolist())

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

componentes = np.arange(1, proporcion.size + 1)
ejes[0].bar(componentes, proporcion, color=AZUL, width=0.62, zorder=2)
ejes[0].plot(componentes, acumulada, color=ROJO, marker="o", markersize=4.5,
             linewidth=1.7, zorder=3)
for c, a in zip(componentes[:3], acumulada[:3]):
    ejes[0].text(c, a + 0.045, f"{a:.2f}".replace(".", ","), color=ROJO, fontsize=8.5,
                 ha="center")
anotar(ejes[0], "las tres primeras ya suman\nel 94 % de la varianza",
       xy=(3, acumulada[2]), xytext=(0.33, 0.42), color=ROJO)
anotar(ejes[0], "estas cinco apenas\naportan nada",
       xy=(7.0, 0.010), xytext=(0.52, 0.28), color=AZUL)
titulo(ejes[0], "Cada componente recoge menos varianza",
       "barras: cuota de esa dirección; línea roja: suma acumulada")
ejes[0].set_xlabel("componente (de la 1ª a la 8ª)")
ejes[0].set_ylabel("proporción de varianza")
ejes[0].set_xticks(componentes)
ejes[0].set_ylim(0, 1.14)
rejilla(ejes[0])
numeros(ejes[0])

# --- Derecha: las seis observaciones del ejemplo de la página, con sus dos direcciones.
x = np.array([1.0, 2, 3, 4, 5, 6])
y = np.array([2.0, 3, 5, 4, 6, 7])
P = np.column_stack([x, y])
centro = P.mean(axis=0)
Q = P - centro                                 # centrar: la nube gira alrededor de su media
S2 = Q.T @ Q / (Q.shape[0] - 1)
val2, vec2 = np.linalg.eigh(S2)                # eigh devuelve los autovalores SIN ordenar
orden = np.argsort(val2)[::-1]                 # de mayor a menor: PC1 primero
val2, vec2 = val2[orden], vec2[:, orden]
print("varianza 2D:", np.round(val2, 2).tolist(),
      "proporción:", np.round(val2 / val2.sum(), 3).tolist())

largo1, largo2 = 2.6, 1.15
ejes[1].plot([centro[0] - largo1 * vec2[0, 0], centro[0] + largo1 * vec2[0, 0]],
             [centro[1] - largo1 * vec2[1, 0], centro[1] + largo1 * vec2[1, 0]],
             color=ROJO, linewidth=1.8, zorder=2)
ejes[1].plot([centro[0] - largo2 * vec2[0, 1], centro[0] + largo2 * vec2[0, 1]],
             [centro[1] - largo2 * vec2[1, 1], centro[1] + largo2 * vec2[1, 1]],
             color=MORADO, linewidth=1.4, linestyle="--", zorder=2)
proyeccion = centro + np.outer(Q @ vec2[:, 0], vec2[:, 0])   # sombra de cada punto en PC1
for p, s in zip(P, proyeccion):
    ejes[1].plot([p[0], s[0]], [p[1], s[1]], color=REJILLA, linewidth=1.0, zorder=1)
ejes[1].scatter(P[:, 0], P[:, 1], s=42, color=AZUL, zorder=4)
ejes[1].scatter(proyeccion[:, 0], proyeccion[:, 1], s=42, facecolor="none",
                edgecolor=ROJO, linewidth=1.4, zorder=4)
ejes[1].text(centro[0] + 2.75, centro[1] + 3.05, "PC1: 97 % de la varianza", color=ROJO,
             fontsize=8.5, ha="center", va="center")
ejes[1].text(centro[0] + 1.75, centro[1] - 1.35, "PC2: 3 %", color=MORADO, fontsize=8.5,
             ha="center", va="center")
anotar(ejes[1], "el círculo es el punto ya reducido;\nla línea gris, lo que se tira",
       xy=(proyeccion[3, 0], proyeccion[3, 1] + 0.05), xytext=(0.22, 0.10), color=TEXTO)
titulo(ejes[1], "Proyectar es quedarse con la sombra",
       "cada punto pasa a ser su posición sobre la recta roja")
ejes[1].set_xlabel("variable 1 (x)")
ejes[1].set_ylabel("variable 2 (y)")
ejes[1].set_xlim(x.min() - 1.0, x.max() + 1.0)
ejes[1].set_ylim(y.min() - 1.6, y.max() + 1.6)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")

guardar(fig, "pca-varianza-y-proyección")
