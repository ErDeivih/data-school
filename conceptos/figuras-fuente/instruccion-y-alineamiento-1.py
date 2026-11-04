"""instruccion-y-alineamiento-1.py — el margen de DPO y la penalización KL: los dos
frenos que impiden que el modelo se aleje para exprimir la recompensa. pagina f08."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(9.4, 4.0))

# --- Panel izquierdo: la perdida de DPO frente al margen ---------------------
sigma = lambda z: 1 / (1 + np.exp(-z))
perdida_dpo = lambda m: -np.log(sigma(m))
margen = np.linspace(-3, 3, 300)

ejes[0].plot(margen, perdida_dpo(margen), color=AZUL, linewidth=1.8)
for m, color in [(0.070, VERDE), (-0.070, ROJO)]:
    ejes[0].plot([m], [perdida_dpo(m)], "o", color=color, markersize=6)

ejes[0].axvline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
# La curva cae en picado: a la derecha del minimo queda un hueco grande y ahi caben las dos
# notas, cada una con su flecha al punto que senalan.
anotar(ejes[0], "margen +0,070\npérdida 0,659", xy=(0.070, perdida_dpo(0.070)),
       xytext=(0.60, 0.86), color=VERDE)
anotar(ejes[0], "margen -0,070\npérdida 0,729", xy=(-0.070, perdida_dpo(-0.070)),
       xytext=(0.60, 0.58), color=ROJO)
anotar(ejes[0], "en margen 0 la pérdida es ln 2", xy=(0.0, perdida_dpo(0.0)),
       xytext=(0.04, 0.07), color=TEXTO, flecha=False)
ejes[0].set_xlabel("margen: sube la preferida menos la descartada")
ejes[0].set_ylabel("pérdida")
ejes[0].set_ylim(0, 3.3)
titulo(ejes[0], "Más margen, menos pérdida en DPO",
       "premia subir la buena más que bajar la mala")
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel derecho: que se lleva la recompensa y que se lleva la penalizacion -
beta = 0.05
recompensas = np.linspace(0.5, 2.0, 100)
for kl, color in [(2.0, AZUL), (20.0, NARANJA)]:
    ejes[1].plot(recompensas, recompensas - beta * kl, color=color, linewidth=1.8,
                 label=f"divergencia KL = {kl:.0f}")

ejes[1].plot([1.2, 1.8], [1.2 - beta * 2.0, 1.8 - beta * 20.0], "o", color=ROJO,
             markersize=6, linestyle="none")
ejes[1].axhline(1.100, color=MORADO, linewidth=1.0, linestyle=":")
# Las dos rectas suben y dejan libre la esquina de abajo a la derecha: la leyenda va ahi y
# las notas en la banda de arriba, por encima de la recta azul.
ejes[1].legend(loc="lower right")
anotar(ejes[1], "subir la recompensa de 1,2 a 1,8\ncuesta 1,0 de KL: el objetivo baja",
       xy=(1.2, 1.2 - beta * 2.0), xytext=(0.03, 0.93), color=ROJO)
anotar(ejes[1], "objetivo 1,100 del ejemplo", xy=(0.5, 1.100), xytext=(0.03, 0.71),
       color=MORADO, flecha=False)
ejes[1].set_xlabel("recompensa r(x, y)")
ejes[1].set_ylabel("objetivo (recompensa menos KL)")
ejes[1].set_ylim(-1.2, 2.3)
titulo(ejes[1], "Sin penalización, la recompensa se exprime",
       "el texto degenera; la penalización KL es el freno")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "instruccion-dpo-y-freno-de-divergencia")
