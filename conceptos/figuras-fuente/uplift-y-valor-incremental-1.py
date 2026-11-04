"""uplift-y-valor-incremental-1.py — la media del grupo tratado esconde quien responde de verdad.
La figura de la pagina de uplift y valor incremental (fase 6)."""

import numpy as np

from comun import *

estilo()

# Tres segmentos con el mismo tratamiento: la tasa de conversion que se ve en cada grupo
segmentos = ["A", "B", "C"]
control = np.array([32.0, 8.0, 22.0])      # % que convierte sin campana
tratado = np.array([6.0, 32.0, 27.0])      # % que convierte con campana
efecto = tratado - control                 # el uplift, en puntos porcentuales
pesos = np.array([10.0, 60.0, 30.0])       # tamano de cada segmento
medio = float(np.sum(pesos * efecto) / pesos.sum())

fig, ejes = plt.subplots(1, 2, figsize=(7.4, 3.8))

# --- Panel izquierdo: lo que se ve si solo miras cada grupo -------------------
ax = ejes[0]
for i, s in enumerate(segmentos):
    color = VERDE if efecto[i] > 0 else ROJO
    ax.plot([0, 1], [control[i], tratado[i]], color=color, linewidth=2.0, marker="o",
            markersize=6)
    ax.text(1.04, tratado[i], f"  segmento {s}", color=color, fontsize=9, va="center")
ax.set_xticks([0, 1], ["sin campana", "con campana"])
ax.set_xlim(-0.15, 1.55)
ax.set_ylim(0, 40)
ax.set_ylabel("% que convierte")
anotar(ax, "aqui la campana va en contra", (0, control[0]), (0.02, 0.95), color=ROJO)
titulo(ax, "Cada segmento responde distinto", "misma campana, efectos de signo opuesto")
rejilla(ax)
numeros(ax, ejes="y")
ax.set_xticks([0, 1], ["sin campaña", "con campaña"])

# --- Panel derecho: repartir el presupuesto exige el efecto, no la tasa -------
ax = ejes[1]
ax.bar(segmentos, efecto, color=[ROJO, VERDE, ROJO], width=0.55)
ax.axhline(2.0, color=TEXTO, linewidth=1.0, linestyle="--")
ax.axhline(medio, color=MORADO, linewidth=1.2, linestyle=":")
anotar(ax, "efecto medio: 13,3 puntos", (1.0, medio), (0.30, 0.95), color=MORADO, flecha=False)
anotar(ax, "por debajo de 2 puntos no compensa", (2.0, 2.0), (0.18, 0.12), color=ROJO)
ax.set_ylim(-32, 32)
ax.set_ylabel("puntos porcentuales de uplift")
titulo(ax, "El promedio no decide a quien atacar", "solo el segmento B supera el umbral")
rejilla(ax)
numeros(ax, ejes="y")
ax.set_xticks([0, 1, 2], segmentos)

guardar(fig, "uplift-efecto-por-segmento")
