"""gnn-1.py — el sobre-suavizado al apilar capas y el reparto de peso de la normalización
simétrica. La figura de la pagina de redes sobre grafos (fase 7)."""

import numpy as np
from matplotlib.ticker import FuncFormatter

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(9.4, 3.9))

# --- Panel 1: sobre-suavizado, medido como el coseno medio entre pares de nodos ---
# Las capas se ponen en posiciones equiespaciadas: en escala logaritmica las etiquetas
# 4, 6 y 8 quedan pegadas y se leen mal.
capas = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]
posicion = np.arange(len(capas))
coseno = np.array([-0.0625, -0.0415, 0.0121, 0.0979, 0.3824, 0.7973, 0.9754, 0.9941, 0.9997, 0.9999])
ejes[0].plot(posicion, coseno, color=AZUL, linewidth=2.0, marker="o", markersize=4.0)
ejes[0].axhline(0.9, color=ROJO, linewidth=1.1, linestyle="--")
titulo(ejes[0], "Todos los nodos acaban pareciendose",
       "a partir de 8 capas el coseno medio pasa de 0,8")
ejes[0].set_xticks(posicion)
ejes[0].set_xticklabels([str(c) for c in capas])
ejes[0].set_xlabel("número de capas apiladas")
ejes[0].set_ylabel("coseno medio entre pares de nodos")
anotar(ejes[0], "aqui las tareas por nodo ya son imposibles", xy=(7, 0.9997), xytext=(0.05, 0.55), color=ROJO)
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel 2: peso de una arista segun el grado de sus extremos ---
d = np.linspace(1.5, 400, 400)
lineal = 1.0 / d                                 # normalizacion por suma de filas
simetrica = 1.0 / np.sqrt(d * d)                 # D^-1/2 A D^-1/2: divide por la raiz del producto
ejes[1].plot(d, lineal, color=AZUL, linewidth=2.0)
ejes[1].plot(d, simetrica, color=NARANJA, linewidth=2.0, linestyle="--")
ejes[1].set_xscale("log")
ejes[1].set_yscale("log")
# Como las dos curvas son la misma funcion, lo que cambia es como se lee el grado.
ejes[1].xaxis.set_major_formatter(FuncFormatter(lambda v, _p: "%g" % v))
ejes[1].set_xticks([2, 5, 10, 25, 50, 100, 200, 400])
titulo(ejes[1], "Cuanto más grado, menos peso por vecino",
       "las dos curvas coinciden: lo que cambia es que se divide por la raiz")
ejes[1].set_xlabel("grado del nodo (escala logaritmica)")
ejes[1].set_ylabel("peso de cada vecino en la suma")
anotar(ejes[1], "un nodo de grado 400 aporta 250 veces menos por arista", xy=(400, simetrica[-1]), xytext=(0.04, 0.24), color=NARANJA)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "gnn-sobresuavizado-y-pesos")
