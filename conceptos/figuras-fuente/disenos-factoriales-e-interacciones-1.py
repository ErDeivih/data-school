"""disenos-factoriales-e-interacciones-1.py - lo que se ve (y lo que no) cuando hay interacción.

Izquierda: dos factores SIN interacción. El catalizador antiguo y el nuevo no se distinguen (las
dos rectas arrancan en el mismo punto) y subir la temperatura anade los mismos 8 puntos en los
dos casos: las rectas son paralelas. El efecto principal de la temperatura es +8 y describe bien
las dos situaciones.
Derecha: dos factores CON interacción. Con el catalizador antiguo la temperatura alta mejora el
rendimiento en 6 puntos, y con el nuevo lo empeora en 9. Las rectas se cruzan: el efecto principal
de la temperatura es el promedio, -1,5, y no describe ninguna de las dos rectas.
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))
temperaturas = np.array([160.0, 220.0])

# --- Izquierda: paralelas, interaccion nula.
ax = ejes[0]
antiguo = np.array([70.0, 78.0])
nuevo = np.array([70.0, 78.0])
ax.plot(temperaturas, antiguo, marker="o", color=AZUL, linewidth=2.0, markersize=7,
        label="catalizador antiguo")
ax.plot(temperaturas, nuevo, marker="s", color=NARANJA, linewidth=2.0, markersize=7,
        linestyle="--", label="catalizador nuevo")
ax.set_xticks(temperaturas, labels=["baja\n(160 °C)", "alta\n(220 °C)"])
ax.set_xlabel("temperatura")
ax.set_ylabel("rendimiento")
ax.set_ylim(62.0, 86.0)
ax.legend(loc="lower right")
anotar(ax, "las dos rectas suben lo mismo:\nel efecto de la temperatura\nno depende del catalizador",
       (220.0, 78.0), (0.05, 0.72), color=TEXTO)
titulo(ax, "Sin interacción: rectas paralelas", "efecto de la temperatura: +8 en los dos catalizadores")
rejilla(ax)
numeros(ax, ejes="y")

# --- Derecha: las rectas se cruzan.
ax = ejes[1]
antiguo = np.array([52.0, 58.0])
nuevo = np.array([60.0, 51.0])
ax.plot(temperaturas, antiguo, marker="o", color=AZUL, linewidth=2.0, markersize=7,
        label="catalizador antiguo")
ax.plot(temperaturas, nuevo, marker="s", color=NARANJA, linewidth=2.0, markersize=7,
        linestyle="--", label="catalizador nuevo")
ax.scatter([188.0], [55.25], marker="D", color=ROJO, s=40, zorder=5)
ax.set_xticks(temperaturas, labels=["baja\n(160 °C)", "alta\n(220 °C)"])
ax.set_xlabel("temperatura")
ax.set_ylabel("rendimiento")
ax.set_ylim(46.0, 67.0)
ax.legend(loc="lower left")
anotar(ax, "la media de las cuatro celdas es −1,5,\ny no cae sobre ninguna de las dos rectas",
       (188.0, 55.25), (0.62, 0.90), color=ROJO)
# Las dos pendientes se etiquetan arriba a la izquierda, en la zona vacía del panel.
ax.text(172.0, 64.6, "nuevo: −9", color=NARANJA, fontsize=8.5, ha="center", va="center")
ax.text(172.0, 61.9, "antiguo: +6", color=AZUL, fontsize=8.5, ha="center", va="center")
titulo(ax, "Con interacción: las rectas se cruzan",
       "el efecto de la temperatura cambia de signo según el catalizador")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "factoriales-interaccion-paralelas-y-cruzadas")
