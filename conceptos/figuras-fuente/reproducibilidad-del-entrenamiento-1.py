"""reproducibilidad-del-entrenamiento-1.py — treinta semillas de la misma configuración y la
diferencia entre predecir la media y predecir la próxima ejecución. La figura de
reproducibilidad del entrenamiento (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Treinta ejecuciones de la MISMA configuracion: lo unico que cambia es la semilla
acc = 0.841 + azar.normal(0, 0.0082, 30)
media, s = acc.mean(), acc.std(ddof=1)
semillas = np.arange(1, 31)

fig, ejes = plt.subplots(1, 2, figsize=(8.4, 3.9))

# --- Izquierda: cada semilla es un entrenamiento entero, y el resultado se mueve ---
ax = ejes[0]
ax.axhspan(media - 2 * s, media + 2 * s, color=AZUL, alpha=0.10, linewidth=0)
ax.axhline(media, color=AZUL, linewidth=1.5)
ax.plot(semillas, acc, "o", color=REJILLA, markersize=5)
ax.plot([1], [acc[0]], "o", color=ROJO, markersize=8, zorder=5)
ax.set_xlim(0, 31)
ax.set_ylim(0.808, 0.874)
ax.set_xlabel("semilla")
ax.set_ylabel("exactitud al terminar")
anotar(ax, "la semilla 1 es el número que reportarías\nsi solo hubieras hecho una",
       (1, acc[0]), (0.05, 0.86), color=ROJO)
anotar(ax, "aquí cae el 95 % de las ejecuciones", (30, media),
       (0.97, 0.22), color=AZUL, align="right", flecha=False)
titulo(ax, "Treinta semillas de la misma configuración",
       "cada punto es un entrenamiento completo")
rejilla(ax)
numeros(ax, ejes="y")

# --- Derecha: mas semillas afinan la media, pero no la prediccion de una ejecucion nueva ---
ax = ejes[1]
k = np.arange(1, 51)
ax.plot(k, 2 * s / np.sqrt(k), color=AZUL, linewidth=1.9, label="intervalo de la media")
ax.plot(k, 2 * s * np.sqrt(1 + 1 / k), color=ROJO, linewidth=1.9,
        label="intervalo de una ejecución nueva")
ax.axhline(2 * s, color=REJILLA, linewidth=1.1, linestyle="--")
ax.set_xlim(0, 50)
ax.set_ylim(0, 0.040)
ax.set_xlabel("semillas ejecutadas")
ax.set_ylabel("amplitud del intervalo al 95 %")
ax.legend(loc="upper right", fontsize=8.5)
anotar(ax, "con más semillas la media se conoce\nmejor y mejor",
       (25, 2 * s / np.sqrt(25)), (0.03, 0.55), color=AZUL)
anotar(ax, "pero la próxima ejecución sigue\ncayendo en esta banda",
       (45, 2 * s * np.sqrt(1 + 1 / 45)), (0.97, 0.44), color=ROJO, align="right")
titulo(ax, "Más semillas afinan la media, no el run",
       "amplitud del intervalo según el número de semillas")
rejilla(ax)
numeros(ax, ejes="both")

guardar(fig, "reproducibilidad-semillas-e-intervalos")
