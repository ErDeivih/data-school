"""sobreajuste-en-redes-1.py — la curva de validación marca dónde parar y la capacidad
tiene un punto dulce. La figura de la página de sobreajuste en redes (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Curvas verosímiles de un entrenamiento: 60 ejemplos, ruido gaussiano de desviación 0,3.
# La pérdida de validación no puede bajar del ruido irreducible, 0,3² = 0,09.
epocas = np.arange(0, 3200, 50)
irreducible = 0.09
train_ruido = azar.normal(0, 0.004, epocas.size)
val_ruido = azar.normal(0, 0.004, epocas.size)
train = irreducible + 0.050 * np.exp(-epocas / 900) + np.cumsum(train_ruido) / 12
val = irreducible + 0.008 + 0.085 * (epocas - 600) ** 2 / (2400.0 ** 2) + val_ruido

fig, ejes = plt.subplots(1, 2, figsize=(8.4, 3.9))

# --- Izquierda: las dos curvas y el hueco entre ellas ---
ax = ejes[0]
ax.plot(epocas, train, color=AZUL, linewidth=1.7, label="entrenamiento")
ax.plot(epocas, val, color=ROJO, linewidth=1.7, label="validación")
ax.axhline(irreducible, color=REJILLA, linewidth=1.1, linestyle=":")
ax.axvline(600, color=REJILLA, linewidth=1.1, linestyle="--")
ax.set_xlim(0, 3150)
ax.set_ylim(0.075, 0.235)
ax.set_xlabel("épocas de entrenamiento")
ax.set_ylabel("pérdida media")
ax.legend(loc="lower right", fontsize=8.5)
anotar(ax, "el ruido irreducible: 0,3² = 0,09;\nlo que baja por debajo es memorización",
       (2600, irreducible), (0.02, 0.75), color=TEXTO, flecha=False)
anotar(ax, "seguir entrenando solo abre el hueco",
       (2600, 0.125), (0.97, 0.97), color=AZUL, flecha=False, align="right")
titulo(ax, "La validación sube mientras el entrenamiento baja",
       "el mínimo de validación decide cuándo parar")
rejilla(ax)
numeros(ax, ejes="y")

# --- Derecha: qué pasa al mover la capacidad del modelo ---
ax = ejes[1]
unidades = np.array([2, 4, 8, 16, 32, 64, 128, 256])
entrena = np.array([0.155, 0.105, 0.093, 0.086, 0.079, 0.073, 0.068, 0.064])
valida = np.array([0.190, 0.140, 0.112, 0.094, 0.107, 0.125, 0.148, 0.172])

ax.semilogx(unidades, entrena, "o-", color=AZUL, markersize=5, linewidth=1.6,
            label="pérdida de entrenamiento")
ax.semilogx(unidades, valida, "o-", color=ROJO, markersize=5, linewidth=1.6,
            label="pérdida de validación")
ax.plot([16], [0.094], "o", color=VERDE, markersize=11, zorder=5)
ax.axvline(16, color=REJILLA, linewidth=1.1, linestyle="--")
ax.set_xticks(unidades)
ax.set_xticklabels([str(u) for u in unidades])
ax.set_xlim(1.5, 340)
ax.set_ylim(0.04, 0.235)
ax.set_xlabel("capacidad: unidades de la capa oculta")
ax.set_ylabel("pérdida media")
ax.legend(loc="upper center", fontsize=8.5)
anotar(ax, "punto dulce: 16 unidades", (16, 0.094), (0.62, 0.20), color=VERDE)
titulo(ax, "Más capacidad no es mejor después del punto dulce",
       "el hueco se abre por la derecha: el entrenamiento sigue bajando")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "sobreajuste-curvas-y-capacidad")
