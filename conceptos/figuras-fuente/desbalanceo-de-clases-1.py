"""desbalanceo-de-clases-1.py — por qué el accuracy enganna con clases raras y que se
gana bajando el umbral. La figura de la pagina de desbalanceo de clases (fase 5)."""

import numpy as np

from comun import *

estilo()

n = 10_000
positivos = 100
# El modelo que predice siempre "no": acierta todo menos los 100 positivos.
tn, fn = n - positivos, positivos

# Los tres umbrales del ejemplo: senalados, positivos encontrados y precision.
umbrales = [0.90, 0.50, 0.10]
senalados = [2, 24, 85]
recall = [0.10, 0.50, 0.90]
precision = [1.00, 0.42, 0.21]

fig, ejes = plt.subplots(1, 2, figsize=(8.2, 3.9), gridspec_kw={"width_ratios": [0.85, 1.15]})

# --- Izquierda: el truco del accuracy ----------------------------------------
ax = ejes[0]
ax.barh([0.0], [tn], color=REJILLA, height=0.55)
ax.barh([0.0], [fn], left=[tn], color=ROJO, height=0.55)
ax.set_xlim(0, n * 1.04)
ax.set_ylim(-0.85, 0.95)
ax.set_yticks([])
ax.set_xlabel("los 10.000 casos")
anotar(ax, f"los {tn:,} negativos:\naqui acierta todo".replace(",", "."), (tn / 2, 0.32),
       (0.30, 0.80), color=TEXTO, flecha=False)
anotar(ax, f"los {fn} fraudes que no ve", (tn + fn / 2, 0.0), (0.85, 0.62), color=ROJO,
       align="right")
ax.text(0.02, -0.62, "accuracy = 9.900 / 10.000 = 0,9900", fontsize=10, color=AZUL)
ax.text(0.02, -0.78, "exhaustividad = 0 / 100 = 0,0000", fontsize=10, color=ROJO)
titulo(ax, "El 99 % de acierto no senala a nadie",
       "predecir siempre «no» ya da ese resultado")
numeros(ax, ejes="x")

# --- Derecha: que pasa cuando se mueve el umbral -----------------------------
ax = ejes[1]
ax.plot(recall, precision, "o-", color=AZUL, markersize=7, linewidth=1.5)
for x, y, t in zip(recall, precision, umbrales):
    ax.annotate(f"umbral {t:.1f}".replace(".", ","), xy=(x, y), xytext=(0, 10),
                textcoords="offset points", fontsize=8.5, color=TEXTO, ha="center")
ax.axhline(0.5, color=REJILLA, linewidth=1.0, linestyle=":")
ax.set_xlim(0, 1.02)
ax.set_ylim(0, 1.16)
ax.set_xlabel("exhaustividad: cuantos fraudes pillo")
ax.set_ylabel("precisión: cuantos de los senalados lo son")
anotar(ax, "bajando a 0,1 se pillan 8 fraudes más, a cambio de 53 falsas alarmas",
       (0.90, 0.21), (0.97, 0.07), color=VERDE, align="right")
titulo(ax, "El umbral mueve el modelo entero",
       "el mismo modelo, tres listones distintos")
rejilla(ax)
numeros(ax)

guardar(fig, "desbalanceo-accuracy-y-umbral")
