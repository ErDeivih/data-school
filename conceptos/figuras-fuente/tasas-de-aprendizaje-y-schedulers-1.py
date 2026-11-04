"""tasas-de-aprendizaje-y-schedulers-1.py — qué hace cada plan con la tasa y cuándo el
entrenamiento se descontrola.

Izquierda: cuatro planes sobre el mismo presupuesto de 1000 pasos, con la tasa normalizada
respecto a su máximo. Los escalones dan saltos, el coseno baja suave y el calentamiento retrasa
la subida para no dar pasos grandes cuando el optimizador aún no sabe nada.
Derecha: f(θ) = θ² desde θ = 1. El error se multiplica por (1 − 2η) en cada paso, así que con
η = 0,5 el factor se anula y con η = 1,1 el signo alterna y la magnitud crece.
La figura de la página de tasas de aprendizaje y planificadores (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: los planes sobre el mismo presupuesto ---------------------------------
ax = ejes[0]
pasos = np.arange(0, 1001)
progreso = pasos / 1000.0

constante = np.ones_like(progreso)
escalones = 0.1 ** (pasos // 250)                       # ×0,1 cada 250 pasos
coseno = 0.5 * (1 + np.cos(np.pi * progreso))
calentamiento = np.where(pasos < 100, pasos / 100.0,
                         0.5 * (1 + np.cos(np.pi * (pasos - 100) / 900.0)))

for valores, color, etiqueta in ((constante, REJILLA, "constante"),
                                 (escalones, ROJO, "escalones"),
                                 (coseno, VERDE, "coseno"),
                                 (calentamiento, MORADO, "calentamiento + coseno")):
    ax.plot(pasos, valores, color=color, linewidth=1.9, label=etiqueta)
anotar(ax, "el calentamiento sube\ndurante 100 pasos", xy=(50.0, 0.5), xytext=(0.02, 0.03),
       color=MORADO)
anotar(ax, "el coseno se desploma\nal final del ciclo", xy=(880.0, coseno[880]),
       xytext=(0.56, 0.03), color=VERDE)
titulo(ax, "Cuatro planes sobre los mismos 1000 pasos",
       "tasa de aprendizaje dividida entre su valor máximo")
ax.set_xlabel("paso de entrenamiento")
ax.set_ylabel("tasa, relativa al máximo")
ax.set_ylim(-0.32, 1.30)
ax.legend(loc="upper center", ncol=2)
rejilla(ax)
numeros(ax)

# --- Derecha: la tasa decide si el error se apaga o explota ---------------------------
ax = ejes[1]
for eta, color in ((0.1, AZUL), (0.5, VERDE), (1.1, ROJO)):
    theta = [1.0]
    for _ in range(10):
        theta.append(theta[-1] - eta * 2 * theta[-1])   # paso de f(θ) = θ²
    ax.plot(np.arange(11), theta, color=color, linewidth=1.9, marker="o", markersize=4,
            label=f"η = {eta:.1f}".replace(".", ","))
ax.axhline(0.0, color=TEXTO, linewidth=0.8, alpha=0.35)
# symlog porque las tres trayectorias viven en escalas muy distintas y una de ellas pasa por 0
ax.set_yscale("symlog", linthresh=1e-3)
anotar(ax, "η = 1,1: el signo alterna\ny crece ×1,2 por paso", xy=(10.0, 1.2 ** 10),
       xytext=(0.58, 0.93), color=ROJO)
anotar(ax, "η = 0,5: el factor es 0\ny acierta en un paso", xy=(1.0, 0.0), xytext=(0.03, 0.06),
       color=VERDE)
titulo(ax, "Con η alta el error crece en cada paso",
       "θ tras cada paso minimizando θ² desde 1")
ax.set_xlabel("paso")
ax.set_ylabel("θ")
ax.set_ylim(-1e4, 1e4)
ax.legend(loc="upper left")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "tasas-de-aprendizaje-y-schedulers-planes-y-divergencia")
