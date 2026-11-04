"""busqueda-binaria-1.py — lo que cuesta partir por la mitad, y cómo encoge el rango paso a paso.
La figura de la página de búsqueda binaria (fase 10).

Izquierda: comparaciones en el peor caso de la búsqueda lineal y de la binaria, de mil a mil
millones de elementos. La lineal es una recta de pendiente 1 en escala logarítmica; la binaria
solo sube una comparación cada vez que la entrada se duplica.
Derecha: la traza real de una búsqueda sobre 16 elementos ordenados buscando el último, que es
el peor caso: el rango vivo se parte en 16, 8, 4, 2 y 1 candidato.
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# --- Izquierda: el coste de las dos búsquedas, del peor caso --------------------------
ax = ejes[0]
n = np.logspace(1, 9, 200)
ax.plot(n, n, color=ROJO, linewidth=1.9, label="búsqueda lineal: hasta n comparaciones")
ax.plot(n, np.log2(n), color=AZUL, linewidth=1.9, label="búsqueda binaria: hasta log₂ n")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(1.5, 4e9)
ax.set_xlim(8, 2e9)
anotar(ax, "mil millones de elementos: mil millones\nde comparaciones frente a 30",
       xy=(1e9, 1e9), xytext=(0.16, 0.20), color=ROJO, flecha=False)
anotar(ax, "pasar de mil a un millón solo añade\ndiez comparaciones a la binaria",
       xy=(1e6, 20), xytext=(0.34, 0.78), color=AZUL)
titulo(ax, "El logaritmo aplana la curva",
       "comparaciones en el peor caso, en escala logarítmica en los dos ejes")
ax.set_xlabel("elementos ordenados entre los que se busca")
ax.set_ylabel("comparaciones")
ax.legend(loc="upper left")
rejilla(ax)
numeros(ax)

# --- Derecha: la traza de una búsqueda real, paso a paso ------------------------------
ax = ejes[1]
valores = [3, 7, 11, 18, 24, 31, 42, 56, 60, 63, 71, 79, 88, 90, 97, 99]
objetivo = valores[-1]                      # el último: el peor caso de la binaria
izq, der, traza = 0, len(valores) - 1, []
while izq <= der:
    medio = (izq + der) // 2
    traza.append((izq, der, medio))
    if valores[medio] == objetivo:
        break
    if valores[medio] < objetivo:
        izq = medio + 1
    else:
        der = medio - 1

for paso, (i, d, m) in enumerate(traza, start=1):
    # El rango que sigue vivo, en ancho, y el centro que se compara en ese paso.
    ax.plot([i - 0.4, d + 0.4], [paso, paso], color=AZUL, linewidth=7, alpha=0.20,
            solid_capstyle="butt", zorder=1)
    ax.plot([m], [paso], marker="o", markersize=8, color=ROJO, zorder=4)
    ax.text(d + 0.7, paso, f"quedan {d - i + 1}", fontsize=8, color=TEXTO, va="center")
ax.plot([traza[-1][2]], [len(traza)], marker="o", markersize=9, color=VERDE, zorder=5)
anotar(ax, "cada paso parte el rango por la mitad:\n16 → 8 → 4 → 2 → 1 candidatos",
       xy=(traza[0][2], 1), xytext=(0.03, 0.30), color=AZUL, flecha=False)
anotar(ax, "el 99 aparece en el paso 5:\nes el peor caso de la búsqueda",
       xy=(15, len(traza)), xytext=(0.36, 0.13), color=VERDE)
titulo(ax, "El rango vivo encoge por la mitad",
       "traza real buscando el 99 entre 16 valores ordenados, que es el peor caso")
ax.set_xticks(range(len(valores)))
numeros(ax, ejes="x")
# Las etiquetas del eje son los valores del array, no los índices: es lo que se compara.
ax.set_xticklabels([str(v) for v in valores], fontsize=7)
ax.set_xlabel("valor del array, por índice (0 a 15)")
ax.set_ylabel("paso de la búsqueda")
ax.set_yticks(range(1, len(traza) + 1))
ax.set_yticklabels([f"paso {k}" for k in range(1, len(traza) + 1)])
ax.set_ylim(len(traza) + 0.6, 0.4)          # el paso 1 arriba: se lee como se ejecuta
ax.set_xlim(-1.2, 17.6)
rejilla(ax, eje="x")

guardar(fig, "busqueda-binaria-pasos-y-fronteras")
