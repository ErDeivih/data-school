"""funciones-de-activacion-1.py — las cuatro activaciones y, sobre todo, sus derivadas.

Izquierda: sigmoide, tanh, ReLU y GELU sobre la misma preactivación z. Derecha: la derivada
de cada una, que es el factor que multiplica al gradiente cuando vuelve hacia atrás. Ahí se
ve la saturación (las derivadas de sigmoide y tanh se van a cero en los extremos) y el corte
de ReLU (derivada 0 en toda la zona negativa: la neurona muerta).
La figura de la página de funciones de activación (fase 7).
"""

import numpy as np

from comun import *

estilo()

z = np.linspace(-6.0, 6.0, 601)

sigmoide = 1.0 / (1.0 + np.exp(-z))
tangente = np.tanh(z)
relu = np.maximum(0.0, z)
# Aproximación con tanh de GELU, la que usan casi todas las implementaciones
gelu = 0.5 * z * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (z + 0.044715 * z ** 3)))

d_sigmoide = sigmoide * (1.0 - sigmoide)      # σ' = σ(1 − σ), máximo 0,25 en z = 0
d_tangente = 1.0 - tangente ** 2              # tanh' = 1 − tanh²
d_relu = (z > 0).astype(float)                # ReLU' = 1 si z > 0, 0 si z < 0
d_gelu = np.gradient(gelu, z)                 # derivada numérica: más corto que la fórmula

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: las cuatro curvas ----------------------------------------------------
ax = ejes[0]
ax.axhline(0.0, color=TEXTO, linewidth=0.8, alpha=0.4)
ax.plot(z, sigmoide, color=AZUL, linewidth=1.8, label="sigmoide")
ax.plot(z, tangente, color=VERDE, linewidth=1.8, label="tanh")
ax.plot(z, relu, color=ROJO, linewidth=1.8, label="ReLU")
ax.plot(z, gelu, color=NARANJA, linewidth=1.8, label="GELU")
# La banda vacía de este panel es la de abajo a la izquierda: ahí la sigmoide vale ~0,
# el tanh −1 y ReLU y GELU son 0. Las notas caben sin pisar ninguna curva.
anotar(ax, "en z = −6 la sigmoide ya vale 0,0025:\naplasta todo a (0, 1)",
       xy=(-6.0, 0.0025), xytext=(0.03, 0.13), color=AZUL)
anotar(ax, "de cero hacia arriba ReLU y GELU\nson la misma recta",
       xy=(4.0, 4.0), xytext=(0.30, 0.45), color=TEXTO)
titulo(ax, "Cuatro activaciones, cuatro maneras de doblar",
       "la salida de una neurona después de la combinación lineal")
ax.set_xlabel("preactivación z")
ax.set_ylabel("activación φ(z)")
ax.set_ylim(-1.6, 6.4)
# La leyenda cabe abajo a la derecha porque allí ReLU y GELU ya han subido fuera del encuadre
ax.legend(loc="lower right")
rejilla(ax)
numeros(ax)

# --- Derecha: la derivada, que es lo que decide si el gradiente sobrevive -------------
ax = ejes[1]
ax.axhline(0.0, color=TEXTO, linewidth=0.8, alpha=0.4)
ax.plot(z, d_sigmoide, color=AZUL, linewidth=1.8)
ax.plot(z, d_tangente, color=VERDE, linewidth=1.8)
ax.plot(z, d_relu, color=ROJO, linewidth=1.8)
ax.plot(z, d_gelu, color=NARANJA, linewidth=1.8)
# Las tres notas van donde ninguna derivada llega: la banda de arriba a la izquierda
# (saturación) y la de abajo, que queda libre al dejar el eje por debajo de cero.
anotar(ax, "en los extremos el gradiente\nque vuelve es casi cero",
       xy=(-4.5, 0.001), xytext=(0.02, 0.90), color=VERDE)
anotar(ax, "el máximo de la sigmoide es 0,25,\nen z = 0",
       xy=(0.0, 0.25), xytext=(0.58, 0.53), color=AZUL)
anotar(ax, "ReLU: derivada 0 en toda la zona negativa",
       xy=(-2.5, 0.0), xytext=(0.03, 0.10), color=ROJO, flecha=False)
titulo(ax, "La derivada decide si el gradiente sobrevive",
       "factor que multiplica al error al atravesar cada neurona")
ax.set_xlabel("preactivación z")
ax.set_ylabel("derivada φ'(z)")
ax.set_ylim(-0.30, 1.50)
rejilla(ax)
numeros(ax)

guardar(fig, "activaciones-curvas-y-derivadas")
