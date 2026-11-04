"""complejidad-asintotica-1.py — comparar crecimientos y ver que el orden manda cuando n crece.
La figura de la página de complejidad asintótica (fase 10)."""

import numpy as np

from comun import *

estilo()

# --- Arriba: cinco crecimientos sobre el mismo rango de n, en escala logarítmica ---
n = np.arange(1, 1001)
crecimientos = [
    ("O(1)", np.ones_like(n, dtype=float), REJILLA),
    ("O(log n)", np.log2(n), CIAN),
    ("O(n)", n, AZUL),
    ("O(n log n)", n * np.log2(n), VERDE),
    ("O(n²)", n ** 2, NARANJA),
]

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 6.2))

ax = ejes[0]
for nombre, valores, color in crecimientos:
    ax.plot(n, valores, color=color, linewidth=1.7, label=nombre)
ax.axvline(100, color=TEXTO, linewidth=0.9, linestyle=":", alpha=0.6)
ax.set_xlim(1, 1000)
ax.set_ylim(0.7, 1.4e6)
ax.set_xlabel("tamaño de la entrada n")
ax.set_ylabel("operaciones (escala logarítmica)")
ax.legend(loc="upper left", fontsize=8.5)
anotar(ax, "con n = 100 el cuadrático ya hace 10.000\noperaciones y el logarítmico 7",
       (100, 1e4), (0.97, 0.42), color=NARANJA, align="right")
anotar(ax, "el logarítmico es casi plano: duplicar la\nentrada cuesta una comparación más",
       (900, 10), (0.97, 0.07), color=CIAN, flecha=False, align="right")
titulo(ax, "Cinco crecimientos, del más plano al que se dispara",
       "la escala es logarítmica: si no, no cabrían juntos")
rejilla(ax)
numeros(ax)

# --- Abajo: el mismo problema resuelto con dos órdenes distintos ---
ax = ejes[1]
tamanos = np.array([1e3, 1e4, 1e5, 1e6])
lineal = tamanos * np.log2(tamanos)
cuadratico = tamanos ** 2
ax.loglog(tamanos, lineal, "o-", color=VERDE, markersize=6, linewidth=1.7, label="n log₂ n")
ax.loglog(tamanos, cuadratico, "o-", color=NARANJA, markersize=6, linewidth=1.7, label="n²")
ax.set_xticks(tamanos)
ax.set_xticklabels(["mil", "10 mil", "100 mil", "1 millón"])
ax.set_xlim(700, 1.4e6)
ax.set_ylim(5e3, 2e13)
ax.set_xlabel("tamaño de la entrada")
ax.set_ylabel("operaciones (escala logarítmica)")
ax.legend(loc="center right", fontsize=8.5)
anotar(ax, "con mil elementos el cuadrático ya hace\ndos órdenes más de trabajo que el otro",
       (1e3, 1e6), (0.04, 0.70), color=NARANJA, flecha=False)
anotar(ax, "en un millón la distancia entre las dos\ncurvas es de un factor 75.000",
       (1e6, 2e13), (0.97, 0.28), color=TEXTO, flecha=False, align="right")
titulo(ax, "La misma tarea, dos órdenes de crecimiento",
       "en escala logarítmica cada orden es una pendiente")
rejilla(ax)
numeros(ax)

guardar(fig, "complejidad-crecimientos-y-pendientes")
