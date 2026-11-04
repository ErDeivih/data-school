"""comprensiones-y-generadores-1.py - cuanta memoria ocupa el resultado segun el tamaño de
la entrada: la lista guarda los n elementos, el generador guarda solo el siguiente. La figura
de la pagina de comprensiones y generadores (fase 3)."""

import sys

import numpy as np

from comun import *

estilo()
fig, ax = plt.subplots(figsize=(7.6, 4.0))

tamanos = np.arange(200, 2001, 200)          # en miles de elementos
mem_lista = np.array([sys.getsizeof([0] * int(n * 1000)) for n in tamanos]) / 1024**2
mem_gen = np.array([sys.getsizeof(x * x for x in range(int(n * 1000))) for n in tamanos]) / 1024

ax.plot(tamanos, mem_lista, color=ROJO, linewidth=2.0, marker="o", markersize=4)
ax.plot(tamanos, mem_gen, color=VERDE, linewidth=2.0, marker="o", markersize=4)
ax.set_yscale("log")
ax.set_ylim(0.1, 30)
titulo(ax, "La lista reserva memoria para los n elementos",
       "el generador, para uno solo")
ax.set_xlabel("elementos que pides al rango (miles)")
ax.set_ylabel("memoria del resultado (MB rojo, KB verde)")
# Los dos textos van en la banda vacía entre la curva roja y la línea verde, cada uno a su
# altura, para que no se pisen ni toquen ninguna de las dos.
anotar(ax, "la lista crece con n: 15 MB con dos millones",
       xy=(1600, mem_lista[7]), xytext=(0.45, 0.55), color=ROJO)
anotar(ax, "el generador se queda en unos cientos de bytes",
       xy=(600, mem_gen[2]), xytext=(0.05, 0.37), color=VERDE)
rejilla(ax)
numeros(ax)
guardar(fig, "comprensiones-y-generadores-memoria")
