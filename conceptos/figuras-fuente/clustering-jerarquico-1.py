"""clustering-jerarquico-1.py — el dendrograma, la linea de corte y por qué el enlace
simple encadena dos grupos separados. Pagina de clustering jerarquico (fase 6)."""

import numpy as np
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage

from comun import *

estilo()
azar = np.random.default_rng(7)

# Dos nubes separadas y un punado de puntos sueltos en medio: es el puente que hace que el
# enlace simple una los dos grupos mucho antes de tiempo (encadenamiento).
X = np.vstack([azar.normal([0.0, 0.0], 0.55, (30, 2)),
               azar.normal([5.5, 0.3], 0.55, (30, 2)),
               azar.uniform([2.2, -1.0], [3.2, 1.0], (9, 2))])
ALTURA_CORTE = 2.5          # en las unidades reales de distancia


def pintar(eje, metodo, color, escala):
    """Dibuja el árbol de fusion y devuelve la altura real de la última fusion.

    `escala` solo multiplica el dibujo: los dos árboles tienen alturas reales muy distintas
    (el completo llega a 7,6 y el simple a 1,9) y sin exagerar uno de ellos no se veria nada.
    """
    Z = linkage(X, method=metodo)
    # La tercera columna de Z es la altura de cada fusion: se escala solo esa.
    Z_dibujo = Z.copy()
    Z_dibujo[:, 2] = Z_dibujo[:, 2] * escala
    dendrogram(Z_dibujo, ax=eje, color_threshold=ALTURA_CORTE * escala,
               above_threshold_color=color, no_labels=True, link_color_func=lambda _: color)
    eje.axhline(ALTURA_CORTE * escala, color=ROJO, linewidth=1.5, linestyle="--")
    return float(Z[-1, 2]), fcluster(Z, t=ALTURA_CORTE, criterion="distance")


fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.8))

altura_simple, grupos_simple = pintar(ejes[0], "single", AZUL, 4.0)
altura_completo, grupos_completo = pintar(ejes[1], "complete", NARANJA, 1.0)

n_simple = len(set(grupos_simple))
n_completo = len(set(grupos_completo))

anotar(ejes[0], f"el corte deja {n_simple} grupo:\nel puente ha fundido las dos nubes",
       xy=(10.0, ALTURA_CORTE * 4.0), xytext=(0.05, 0.95), color=AZUL, flecha=False)
anotar(ejes[0], f"la última union de este árbol\nesta a {coma(round(altura_simple, 2))} de distancia",
       xy=(10.0, 0.2), xytext=(0.53, 0.40), color=REJILLA, flecha=False)
titulo(ejes[0], "Enlace simple: manda el par más cercano",
       "cada punto nuevo se engancha al grupo por el vecino que tiene al lado")
ejes[0].set_xlabel("observaciones (reordenadas por el árbol)")
ejes[0].set_ylabel("altura de la fusion (dibujo x4)")
ejes[0].set_ylim(0, 12)
rejilla(ejes[0], eje="y")
numeros(ejes[0], ejes="y")

anotar(ejes[1], f"el mismo corte deja {n_completo} grupos:\naqui las dos nubes no se han fundido",
       xy=(10.0, ALTURA_CORTE), xytext=(0.05, 0.24), color=NARANJA, flecha=False)
anotar(ejes[1], f"la última union de este árbol\nesta a {coma(round(altura_completo, 2))} de distancia",
       xy=(10.0, 0.2), xytext=(0.53, 0.40), color=REJILLA, flecha=False)
titulo(ejes[1], "Enlace completo: manda el par más lejano",
       "un grupo solo admite un punto si esta cerca de todos sus miembros")
ejes[1].set_xlabel("observaciones (reordenadas por el árbol)")
ejes[1].set_ylabel("altura de la fusion")
ejes[1].set_ylim(0, 12)
rejilla(ejes[1], eje="y")
numeros(ejes[1], ejes="y")

guardar(fig, "clustering-jerarquico-dendrograma-y-corte")
