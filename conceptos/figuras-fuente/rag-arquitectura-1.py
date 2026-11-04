"""rag-arquitectura-1.py — tres vistas del mismo problema: la fusion de rangos no
suma puntuaciones, reescribe posiciones, y el techo del sistema lo fija el eslabon
más debil. La figura de la pagina de RAG (fase 8)."""

import numpy as np
from matplotlib.patches import Rectangle

from comun import *

estilo()

# El ejemplo de la pagina, con los dos rankings ya calculados
denso = ["A", "C", "D", "B"]
lexico = ["D", "A", "B", "C"]
fragmentos = ["A", "B", "C", "D"]
k = 60


def rrf(c):
    """Suma 1/(k + posición) en cada ranking. Solo usa posiciones, no puntuaciones."""
    return 1 / (k + denso.index(c) + 1) + 1 / (k + lexico.index(c) + 1)


fusion = sorted(fragmentos, key=lambda c: -rrf(c))

# Dos filas: la lista de los dos rankings necesita alto (ocho cajas con su numero) y la curva
# del techo agradece el ancho entero. En una fila de tres cada panel quedaba estrecho y la
# leyenda y la nota de D se metian encima de las cajas.
fig = plt.figure(figsize=(10.6, 8.6))
rejilla_paneles = fig.add_gridspec(2, 2, height_ratios=[1.45, 1.0])
izq = fig.add_subplot(rejilla_paneles[0, 0])
centro = fig.add_subplot(rejilla_paneles[0, 1])
der = fig.add_subplot(rejilla_paneles[1, :])

# --- Panel de arriba a la izquierda: los dos rankings y el acuerdo que los une ---------
colores_denso = {"A": AZUL, "B": AZUL, "C": ROJO, "D": MORADO}
colores_lexico = {"D": MORADO, "A": AZUL, "B": AZUL, "C": ROJO}

for i, c in enumerate(denso):
    izq.add_patch(Rectangle((0, 2.05 - i), 1.0, 0.7, color=colores_denso[c], alpha=0.85))
    izq.text(-0.12, 2.4 - i, f"{i + 1}.", ha="right", va="center", fontsize=9)
    izq.text(1.15, 2.4 - i, c, va="center", fontsize=9)
# El segundo ranking va un poco mas abajo de lo que estaba: con las dos listas pegadas no se
# veia donde acaba una y empieza la otra.
for i, c in enumerate(lexico):
    izq.add_patch(Rectangle((0, -1.85 - i), 1.0, 0.7, color=colores_lexico[c], alpha=0.85))
    izq.text(-0.12, -1.5 - i, f"{i + 1}.", ha="right", va="center", fontsize=9)
    izq.text(1.15, -1.5 - i, c, va="center", fontsize=9)

izq.plot([-0.35, -0.35], [2.85, -4.9], color=TEXTO, linewidth=0.8)
izq.plot([], [], color=AZUL, linewidth=6, label="busqueda densa")
izq.plot([], [], color=VERDE, linewidth=6, label="busqueda lexica")
# La leyenda se va a la franja de arriba, por encima de la primera caja: abajo a la izquierda
# tapaba los numeros 3 y 4 y la caja B del segundo ranking.
izq.legend(loc="upper center", ncols=2, fontsize=8.5)
# La nota de D tambien cabe en la banda vacia de la izquierda (aqui no hay cajas) y el color
# morado ya la ata a la caja de D, asi que no hace falta flecha.
anotar(izq, "D: tercera para la densa,\nprimera para la lexica", xy=(0.5, -1.5),
       xytext=(0.40, 0.39), color=MORADO, flecha=False, align="right")
izq.set_xlim(-2.2, 2.0)
izq.set_ylim(-5.2, 4.2)
izq.axis("off")
titulo(izq, "Dos buscadores que no coinciden")

# --- Panel de arriba a la derecha: las dos aportaciones y el total ---------------------
pos = np.arange(4)
a_denso = [1 / (k + denso.index(c) + 1) for c in fusion]
a_lexico = [1 / (k + lexico.index(c) + 1) for c in fusion]
total = [rrf(c) for c in fusion]

centro.bar(pos, a_denso, width=0.55, color=AZUL, label="aporta el ranking denso")
centro.bar(pos, a_lexico, bottom=a_denso, width=0.55, color=VERDE, label="aporta el lexico")

for i, c in enumerate(fusion):
    centro.text(i, total[i] + 0.00025, f"{total[i]:.5f}".replace(".", ","),
                ha="center", fontsize=8, color=TEXTO)
centro.set_xticks(pos)
centro.set_xticklabels(fusion)
centro.set_xlabel("fragmento, en orden de fusion")
centro.set_ylabel("RRF: suma de 1 / (k + posición)")
# Un poco más de aire arriba: asi la leyenda no toca los numeros de las barras.
centro.set_ylim(0, max(total) * 1.60)
titulo(centro, "A sube por consenso y C se hunde")
centro.legend(loc="upper left", fontsize=8.5)
rejilla(centro)
numeros(centro, "y")

# --- Panel de abajo: los eslabones se multiplican, no se suman -------------------------
recalls = np.linspace(0.5, 1.0, 100)
for rerank, color in [(0.85, ROJO), (0.95, VERDE), (1.00, AZUL)]:
    der.plot(recalls, recalls * rerank, color=color, linewidth=1.8,
             label=f"reordenación {rerank:.2f}".replace(".", ","))

der.plot([0.92], [0.92 * 0.85], "o", color=ROJO, markersize=6)
# Debajo de la recta roja, a la derecha, no pasa ninguna de las tres lineas.
anotar(der, "el sistema del ejemplo: 0,78", xy=(0.92, 0.92 * 0.85),
       xytext=(0.78, 0.14), color=ROJO)
der.set_xlabel("recall de recuperación")
der.set_ylabel("techo del sistema completo")
der.set_ylim(0.4, 1.06)
titulo(der, "Los eslabones se multiplican, no se suman")
der.legend(loc="upper left")
rejilla(der)
numeros(der)

guardar(fig, "rag-fusion-de-ranks-y-consenso")
