"""series-jerarquicas-1.py — el desajuste entre niveles y qué hace la reconciliación.
La figura de la página de series jerárquicas (fase 5)."""

import numpy as np

from comun import *

estilo()

# Los tres pronósticos base, cada uno de su propio modelo: nacional, tienda A, tienda B.
nacional, a, b = 1200.0, 720.0, 520.0
peso = np.array([a, b]) / (a + b)
rec = peso * nacional                      # reparto proporcional del total

fig, ejes = plt.subplots(1, 2, figsize=(7.4, 3.8))

# --- Panel izquierdo: los pronósticos base no cuadran -------------------------
ax = ejes[0]
ax.bar([0, 1], [a, b], color=AZUL, width=0.55)
altura = a + b
ax.plot([-0.5, 1.5], [altura, altura], color=ROJO, linewidth=1.4)
ax.plot([-0.5, 1.5], [nacional, nacional], color=MORADO, linewidth=1.4, linestyle="--")
ax.set_ylim(0, 1500)
ax.set_ylabel("miles de euros")
anotar(ax, f"la suma da {altura:.0f}", (0.5, altura), (0.30, 0.88), color=ROJO)
anotar(ax, f"el modelo nacional dice {nacional:.0f}", (1.2, nacional), (0.06, 0.60), color=MORADO)
titulo(ax, "Aquí nadie se equivoca: sobran 40", "dos modelos válidos dan totales distintos")
rejilla(ax)
numeros(ax)
ax.set_xticks([0, 1], ["tienda A", "tienda B"])   # después de numeros(), que reescribe las etiquetas

# --- Panel derecho: la misma jerarquía, ya coherente --------------------------
ax = ejes[1]
x = np.arange(3)
ancho = 0.36
ax.bar(x - ancho / 2, [nacional, a, b], ancho, color=REJILLA, label="pronóstico base")
ax.bar(x + ancho / 2, [nacional, rec[0], rec[1]], ancho, color=VERDE, label="tras reconciliar")
ax.set_ylim(0, 1500)
anotar(ax, "el nacional no se toca", (0 - ancho / 2, nacional), (0.03, 0.94), color=MORADO, flecha=False)
anotar(ax, "las tiendas absorben el ajuste", (1 + ancho / 2, rec[0]), (0.30, 0.62), color=VERDE)
ax.legend(loc="upper right")
titulo(ax, "El ajuste se reparte por tamaño", "la tienda grande absorbe más corrección")
rejilla(ax)
numeros(ax)
ax.set_xticks(x, ["nacional", "tienda A", "tienda B"])

guardar(fig, "series-jerarquicas-niveles-y-reconciliación")
