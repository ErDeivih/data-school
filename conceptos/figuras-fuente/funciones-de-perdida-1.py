"""funciones-de-perdida-1.py — qué cobra cada pérdida según lo segura que sea la respuesta.

Izquierda: la pérdida de un ejemplo en función de la probabilidad que el modelo da a la clase
verdadera. La entropía cruzada (BCE) crece sin límite cuando el modelo está seguro y
equivocado; el error cuadrático (MSE) se aplana en 1 y deja de distinguir ese caso.
Derecha: el peso (1 − p)^γ de la pérdida focal, que apaga los ejemplos ya acertados.
La figura de la página de funciones de pérdida (fase 7).
"""

import numpy as np

from comun import *

estilo()

p = np.linspace(0.01, 0.999, 400)          # probabilidad de la clase verdadera
bce = -np.log(p)                            # entropía cruzada binaria de ese ejemplo
mse = (1.0 - p) ** 2                        # error cuadrático de ese ejemplo
focal = (1.0 - p) ** 2 * bce                # focal con γ = 2

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: lo que cuesta cada respuesta -----------------------------------------
ax = ejes[0]
ax.plot(p, bce, color=AZUL, linewidth=1.8, label="entropía cruzada (BCE)")
ax.plot(p, mse, color=ROJO, linewidth=1.8, label="error cuadrático (MSE)")
ax.plot(p, focal, color=NARANJA, linewidth=1.8, label="focal con γ = 2")
ax.set_yscale("log")
ax.set_ylim(1e-3, 6.0)          # en escala log la banda de abajo queda libre para las notas
ax.set_xlim(0.0, 1.0)
# Las notas van abajo: en escala logarítmica ahí no hay ninguna curva.
anotar(ax, "seguro y equivocado:\nla BCE cobra 4,6",
       xy=(0.01, 4.605), xytext=(0.05, 0.17), color=AZUL)
anotar(ax, "el MSE se aplana en 1: no distingue\nun error rotundo de uno tibio",
       xy=(0.5, 0.25), xytext=(0.40, 0.075), color=ROJO)
titulo(ax, "La BCE no tiene techo; el MSE sí",
       "pérdida de un ejemplo según la probabilidad de su clase verdadera")
ax.set_xlabel("probabilidad que el modelo da a la clase verdadera")
ax.set_ylabel("pérdida del ejemplo")
ax.legend(loc="upper right")
rejilla(ax)
numeros(ax, ejes="x")

# --- Derecha: el peso que la focal pone a cada ejemplo --------------------------------
ax = ejes[1]
pp = np.linspace(0.0, 1.0, 400)
for gamma, color in ((0.0, AZUL), (2.0, NARANJA), (5.0, MORADO)):
    ax.plot(pp, (1.0 - pp) ** gamma, color=color, linewidth=1.8,
            label=f"γ = {gamma:g}")
anotar(ax, "con γ = 0 la focal es la entropía\ncruzada: todos los ejemplos pesan igual",
       xy=(0.35, 1.0), xytext=(0.97, 0.90), color=AZUL, align="right")
anotar(ax, "con γ = 2 un acierto al 95 %\nya solo pesa 0,0025",
       xy=(0.95, 0.0025), xytext=(0.97, 0.34), color=NARANJA, align="right")
titulo(ax, "La focal apaga los ejemplos ya acertados",
       "peso (1 − p)^γ que multiplica a la entropía cruzada de cada ejemplo")
ax.set_xlabel("probabilidad que el modelo da a la clase verdadera")
ax.set_ylabel("peso del ejemplo")
ax.set_ylim(-0.02, 1.06)
ax.legend(loc="center left")
rejilla(ax)
numeros(ax)

guardar(fig, "perdidas-bce-mse-y-focal")
