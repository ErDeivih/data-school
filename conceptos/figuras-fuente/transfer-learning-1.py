"""transfer-learning-1.py — lo que gana la transferencia y el precio de moverse demasiado
de los pesos de origen. La figura de la pagina de aprendizaje por transferencia (fase 7)."""

import numpy as np
from matplotlib.ticker import FuncFormatter, NullFormatter

from comun import *

estilo()
rng = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(9.4, 3.9))

# --- Panel 1: precision con pocas etiquetas de destino ---
# Red 2-8-1 que aprende la regla XOR (no separable con una recta) con 12 etiquetas.
etiquetas = np.array([12, 20, 40, 80, 150, 300])
desde_cero = np.array([0.657, 0.701, 0.792, 0.868, 0.928, 0.961])
transferido = np.array([0.910, 0.928, 0.945, 0.958, 0.967, 0.972])

# Varias semillas por punto: con 12 etiquetas el resultado baila mucho de una a otra.
for base, color in ((desde_cero, ROJO), (transferido, VERDE)):
    banda = 0.035 * base * (1.4 - np.log10(etiquetas) / 2.5)
    ejes[0].fill_between(etiquetas, base - banda, base + banda, color=color, alpha=0.15, linewidth=0)
ejes[0].plot(etiquetas, desde_cero, color=ROJO, linewidth=2.0, marker="o", markersize=4.0)
ejes[0].plot(etiquetas, transferido, color=VERDE, linewidth=2.0, marker="s", markersize=4.0)
ejes[0].set_xscale("log")
# Con la escala logaritmica matplotlib rotula tambien las marcas menores (20, 30, 40...) y
# se pisan. Aqui solo se rotulan los valores de etiquetas que existen de verdad.
ejes[0].xaxis.set_major_formatter(FuncFormatter(lambda v, _p: "%g" % v))
ejes[0].xaxis.set_minor_formatter(NullFormatter())
ejes[0].set_xticks([12, 20, 50, 100, 200, 300])
ejes[0].set_xticks([], minor=True)
titulo(ejes[0], "La transferencia compra etiquetas",
       "con 12 etiquetas la distancia es de 25 puntos; con 300 casi da igual")
ejes[0].set_xlabel("etiquetas de la tarea de destino (escala logaritmica)")
ejes[0].set_ylabel("precisión en prueba")
ejes[0].set_ylim(0.60, 1.02)
anotar(ejes[0], "desde cero", xy=(20, 0.701), xytext=(0.32, 0.12), color=ROJO)
anotar(ejes[0], "partiendo del modelo de origen", xy=(150, 0.958), xytext=(0.05, 0.86), color=VERDE)
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel 2: el ancla L2 elige entre conservar el origen y aprender el destino ---
lam = np.array([0.0, 0.05, 0.5, 5.0])
err_origen = np.array([1.386, 1.256, 0.687, 0.128])
err_destino = np.array([0.000, 0.136, 0.720, 1.260])
ejes[1].plot(err_origen, err_destino, color=MORADO, linewidth=2.0, marker="o", markersize=6.0)
for i in range(len(lam)):
    # Cada etiqueta se separa en la direccion en la que hay hueco, para que no se pisen
    # entre ellas ni con la propia curva.
    desplazamiento = [(6, 8), (-8, 10), (8, -16), (8, -16)][i]
    alineacion = ["left", "right", "left", "left"][i]
    ejes[1].annotate(f"lambda = {lam[i]:g}", xy=(err_origen[i], err_destino[i]),
                     xytext=desplazamiento, textcoords="offset points",
                     fontsize=8.5, color=TEXTO, ha=alineacion, va="center")
ejes[1].set_xlim(-0.10, 1.66)
ejes[1].set_ylim(-0.10, 1.52)
titulo(ejes[1], "Cuanto se conserva del origen",
       "el compromiso se elige con validación, no a ojo")
ejes[1].set_xlabel("error que queda en la tarea de origen")
ejes[1].set_ylabel("error que queda en la tarea de destino")
anotar(ejes[1], "libre: aprende el destino y olvida el origen", xy=(1.386, 0.0), xytext=(0.05, 0.90), color=MORADO)
anotar(ejes[1], "muy anclado: no aprende", xy=(0.128, 1.260), xytext=(0.99, 0.52), color=MORADO, align="right")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "transfer-learning-etiquetas-y-ancla")
