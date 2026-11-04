"""np-completitud-1.py — la asimetría entre comprobar y encontrar, y el mapa de las clases.
La figura de la página de NP-completitud (fase 10).

Izquierda: buscar un subconjunto que sume un objetivo cuesta 2ⁿ intentos; comprobar el
candidato cuesta n sumas. Las dos curvas viven en escalas distintas y la distancia se abre
sin parar: con 30 números, mil millones de intentos frente a 30 sumas.
Derecha: dónde cae cada problema. P dentro de NP, NP dentro de PSPACE, y los NP-completos
en la franja de NP que quedaría fuera de P si la conjetura P ≠ NP es cierta.
"""

import numpy as np
from matplotlib.patches import Ellipse

from comun import *

estilo()
azar = np.random.default_rng(7)          # semilla fija, por coherencia con el resto

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.6))

# --- Izquierda: lo que cuesta buscar y lo que cuesta verificar ------------------------
ax = ejes[0]
n = np.arange(5, 61)
# Sin leyenda: cada curva se nombra en la nota de su color, en el hueco que deja libre.
ax.semilogy(n, 2.0 ** n, color=ROJO, linewidth=1.9)
ax.semilogy(n, n, color=AZUL, linewidth=1.9)
ax.axhline(4.3e17, color=MORADO, linewidth=1.4, linestyle=":")
ax.set_xlim(5, 63)
ax.set_ylim(1, 1e20)
anotar(ax, "buscar: probar los 2ⁿ subconjuntos.\nCon 30 números, 1.073.741.824 intentos",
       xy=(30, 2.0 ** 30), xytext=(0.04, 0.62), color=ROJO)
anotar(ax, "la línea morada son los segundos que ha\nvivido el universo: 4,3 · 10¹⁷",
       xy=(20, 4.3e17), xytext=(0.03, 0.94), color=MORADO, flecha=False)
anotar(ax, "verificar: sumar el candidato cuesta n,\nasí que la curva azul es casi plana",
       xy=(50, 50), xytext=(0.30, 0.16), color=AZUL)
titulo(ax, "Encontrar cuesta 2ⁿ; comprobar, n",
       "subconjuntos que hay que probar y sumas que cuesta el certificado, según n")
ax.set_xlabel("n: números disponibles para el subconjunto")
ax.set_ylabel("operaciones (escala logarítmica)")
rejilla(ax)
numeros(ax)

# --- Derecha: el mapa de las clases, con un ejemplo y una cifra en cada región --------
ax = ejes[1]
ax.axis("off")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

ax.add_patch(Ellipse((0.50, 0.48), 0.86, 0.70, facecolor=CIAN, alpha=0.06,
                     edgecolor=CIAN, linewidth=1.4))
ax.add_patch(Ellipse((0.42, 0.46), 0.54, 0.50, facecolor=AZUL, alpha=0.08,
                     edgecolor=AZUL, linewidth=1.4))
ax.add_patch(Ellipse((0.34, 0.38), 0.26, 0.24, facecolor=VERDE, alpha=0.14,
                     edgecolor=VERDE, linewidth=1.4))

ax.text(0.50, 0.90, "PSPACE", ha="center", va="center", fontsize=10, color=CIAN)
ax.text(0.50, 0.855, "se resuelve con memoria polinómica", ha="center", va="center",
        fontsize=8, color=CIAN)
ax.text(0.42, 0.785, "NP", ha="center", va="center", fontsize=10, color=AZUL)
ax.text(0.42, 0.740, "la solución se comprueba rápido", ha="center", va="center",
        fontsize=8, color=AZUL)
ax.text(0.34, 0.420, "P", ha="center", va="center", fontsize=10, color=VERDE)
ax.text(0.34, 0.330, "ordenar, Dijkstra,\nprogramación lineal", ha="center", va="center",
        fontsize=7.5, color=VERDE)
ax.text(0.60, 0.560, "NP-completo", ha="center", va="center", fontsize=9.5, color=ROJO)
ax.text(0.60, 0.495, "SAT, viajante, mochila", ha="center", va="center", fontsize=7.5,
        color=ROJO)
ax.text(0.60, 0.435, "SAT con 60 variables:\n1,15 · 10¹⁸ asignaciones", ha="center",
        va="center", fontsize=7.5, color=ROJO)
anotar(ax, "nadie sabe si la franja roja está vacía:\nP = NP sigue abierta desde 1971",
       xy=(0.60, 0.50), xytext=(0.98, 0.06), color=TEXTO, flecha=False, align="right")
anotar(ax, "la parada de una máquina de Turing ni cabe\naquí: no existe algoritmo ninguno",
       xy=(0.50, 0.20), xytext=(0.02, 0.06), color=MORADO, flecha=False)
titulo(ax, "Cada problema, en su caja",
       "las inclusiones demostradas y la franja que depende de una conjetura")

guardar(fig, "np-completitud-verificar-y-buscar")
