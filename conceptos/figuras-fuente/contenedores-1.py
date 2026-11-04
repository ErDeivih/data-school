"""contenedores-1.py — las capas de una imagen se reutilizan si nada de arriba cambia, y las
capas compartidas se guardan una sola vez en disco. La figura de la pagina (fase 11)."""

import numpy as np
from matplotlib.patches import Rectangle

from comun import *

estilo()

# Las cuatro capas del Dockerfile del ejemplo, en MB: base, dependencias y codigo.
tamanos = np.array([150.0, 250.0, 2.0, 2.0])
anchura = tamanos / tamanos.sum()                               # el ancho es la proporcion
limites = np.concatenate([[0.0], np.cumsum(tamanos)[:-1]]) / tamanos.sum()   # inicio de cada capa

fig, ejes = plt.subplots(2, 1, figsize=(8.6, 6.6))

# --- Arriba: que capas sobreviven a cada cambio -------------------------------
# Dos filas con separacion entre ellas, y los rotulos a la izquierda en vez de pegados a la
# barra: asi las anotaciones tienen sitio y no se pisan con los rotulos de las capas.
filas = {"codigo": 2.0, "deps": 0.6}
casos = [("codigo", "cambio en el codigo", 2), ("deps", "cambio en las dependencias", 1)]
for clave, etiqueta, primera_nueva in casos:
    y = filas[clave]
    for i, (ancho, x) in enumerate(zip(anchura, limites)):
        # Verde: la capa sale identica y se reutiliza. Rojo: cambia y hay que reconstruirla.
        color = VERDE if i < primera_nueva else ROJO
        ejes[0].add_patch(Rectangle((x, y - 0.20), ancho, 0.40, facecolor=color,
                                    edgecolor="white", linewidth=0.8))
        if ancho > 0.12:            # dentro solo cabe el texto de las capas anchas
            ejes[0].text(x + ancho / 2, y, f"{tamanos[i]:.0f} MB", ha="center", va="center",
                         fontsize=8.5, color="white")

anotar(ejes[0], "cambiar el pip invalida todo lo que va detras",
       xy=(0.5, 1.5), xytext=(0.13, 0.04), color=ROJO)
anotar(ejes[0], "tocar solo el codigo salva 3 capas de 4",
       xy=(0.88, 1.8), xytext=(0.13, 0.85), color=VERDE)
ejes[0].text(0.0, 2.55, "cambio en el codigo", fontsize=9, color=TEXTO)
ejes[0].text(0.0, 1.15, "cambio en las dependencias", fontsize=9, color=TEXTO)

ejes[0].set_yticks([])
ejes[0].set_ylim(-0.4, 2.9)
ejes[0].set_xlim(0, 1)
ejes[0].set_xlabel("la imagen, repartida por capas")
titulo(ejes[0], "Cada capa depende de las de arriba",
       "un cambio invalida esa capa y todas las que vienen detras")
rejilla(ejes[0], "x")

# --- Abajo: lo que ocupan ocho servicios con la misma base --------------------
# En miles de MB: con el eje en miles y rotulos largos, matplotlib encoge los ejes a cero
# (el ancho del SVG se dispara a 100.000 px) porque el margen pedido no cabe en la figura.
sin_dedup, con_dedup = 3.2, 2.15
for i, (etiqueta, miles, color) in enumerate([("suma de los tamaños de las 8 imagenes", sin_dedup, ROJO),
                                              ("lo que ocupa el disco con capas compartidas", con_dedup, VERDE)]):
    ejes[1].barh(i, miles, height=0.5, color=color)
    ejes[1].text(miles - 0.05, i, f"{miles * 1000:.0f} MB", va="center", ha="right",
                 fontsize=9, color="white")
    ejes[1].text(miles + 0.06, i, etiqueta, va="center", ha="left", fontsize=7.5, color=TEXTO)

anotar(ejes[1], "la capa base de 150 MB se guarda una sola vez: el 32,8 % de ahorro",
       xy=(1.0, 1.7), xytext=(0.04, 0.08), color=VERDE)

ejes[1].set_yticks([])
ejes[1].set_ylim(2.6, -0.7)     # invertido a mano: la fila 0 (3200 MB) queda arriba
ejes[1].set_xlim(0, 5)
ejes[1].set_xlabel("miles de MB")
titulo(ejes[1], "Las capas compartidas no se duplican",
       "el ahorro es lo que hace viable tener veinte servicios sobre la misma base")
rejilla(ejes[1], "x")
numeros(ejes[1], "x")

guardar(fig, "contenedores-capas-y-deducción")
