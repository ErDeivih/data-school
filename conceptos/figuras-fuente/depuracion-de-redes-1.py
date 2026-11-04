"""depuracion-de-redes-1.py — las dos comprobaciones baratas: la pérdida de arranque y el
test de memorizar un lote. La figura de la página de depurar el entrenamiento (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Historial verosímil del test de memorización: 8 ejemplos casi arbitrarios, una capa de 16
# unidades y regularización desactivada. La pérdida de arranque es ln(2) = 0,6931.
epocas = np.arange(0, 601)
base = 0.6931
perdida = base * np.exp(-epocas / 130) + 0.0088 + azar.normal(0, 0.0035, epocas.size)
perdida[0] = base

fig, ejes = plt.subplots(1, 2, figsize=(8.4, 3.9))

# --- Izquierda: memorizar un lote diminuto tiene que bajar dos órdenes ---
ax = ejes[0]
ax.semilogy(epocas, perdida, color=AZUL, linewidth=1.6, label="pérdida sobre los 8 ejemplos")
ax.axhline(base, color=REJILLA, linewidth=1.2, linestyle="--")
ax.set_xlim(0, 600)
ax.set_ylim(0.003, 2.0)
ax.set_xlabel("épocas")
ax.set_ylabel("pérdida (escala logarítmica)")
ax.legend(loc="upper right", fontsize=8.5)
anotar(ax, "arranca en ln 2 = 0,6931:\nlo que vale no saber nada",
       (0, base), (0.03, 0.62), color=TEXTO)
anotar(ax, "si esta curva se queda plana,\nel fallo está en el código, no en los datos",
       (600, 0.0088), (0.97, 0.16), color=ROJO, flecha=False, align="right")
titulo(ax, "Ocho ejemplos: la pérdida debe desplomarse",
       "memorizar un lote diminuto separa bug de datos")
numeros(ax, ejes="x")

# --- Derecha: la pérdida de arranque de referencia es ln C ---
ax = ejes[1]
clases = np.array([2, 10, 100, 1000, 10000])
referencia = np.log(clases)

ax.semilogx(clases, referencia, "o-", color=VERDE, markersize=6, linewidth=1.7,
            label="ln C, la referencia")
ax.plot([10], [6.5759], "o", color=ROJO, markersize=8, zorder=5)
ax.set_xticks(clases)
ax.set_xticklabels([str(c) for c in clases])
ax.set_xlim(1.4, 14000)
ax.set_ylim(0, 10.6)
ax.set_xlabel("clases del clasificador C")
ax.set_ylabel("pérdida en el primer paso")
ax.legend(loc="upper left", fontsize=8.5)
anotar(ax, "logits con desviación 4 dan 6,58:\nla capa de salida está mal escalada",
       (10, 6.5759), (0.97, 0.78), color=ROJO, align="right")
anotar(ax, "una pérdida muy por debajo de la línea\ndelata etiquetas filtradas o mal emparejadas",
       (1000, np.log(1000)), (0.97, 0.14), color=TEXTO, flecha=False, align="right")
titulo(ax, "El primer paso tiene un valor esperado",
       "alejarse de ln C localiza el fallo")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "depuracion-memorizar-y-arranque")
