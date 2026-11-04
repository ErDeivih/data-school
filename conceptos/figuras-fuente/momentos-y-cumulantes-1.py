"""momentos-y-cumulantes-1.py - misma media y misma varianza no es la misma distribución:
lo que cambia, y lo que decide el dinero, esta en la cola. Figura de la pagina de
momentos y cumulantes."""

import numpy as np
from scipy import stats

from comun import *

estilo()

x = np.linspace(-8, 8, 1200)
nu = 5.0
esc = np.sqrt(nu / (nu - 2))                 # escala para que la t(5) tenga varianza 1
normal = stats.norm.pdf(x)
cola = stats.t.pdf(x, nu) / esc
corte = x[np.argmax(cola < normal)]          # a partir de aqui la t pesa mas

fig, ejes = plt.subplots(1, 2, figsize=(10.2, 4.0))

# --- Izquierda: densidad lineal. Las dos curvas se parecen; la diferencia esta al fondo.
ejes[0].plot(x, normal, color=AZUL, linewidth=1.8, label="normal: curtosis de exceso 0")
ejes[0].plot(x, cola, color=ROJO, linewidth=1.6, linestyle="--",
             label="t de Student con 5 grados de libertad: exceso 6")
ejes[0].axvline(-corte, color=TEXTO, linewidth=0.8, alpha=0.5)
ejes[0].axvline(corte, color=TEXTO, linewidth=0.8, alpha=0.5)
ejes[0].annotate("cada 2 % de los casos cae fuera\nde cada una de estas lineas",
                 xy=(-corte, 0.002), xytext=(-8.6, 0.115), color=TEXTO, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9,
                                 connectionstyle="arc3,rad=-0.2"))
ejes[0].annotate("en el centro las dos curvas\nson casi la misma",
                 xy=(-1.6, 0.11), xytext=(-7.0, 0.30), color=TEXTO, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
ejes[0].set_title("Misma media y misma varianza, distinta distribución")
ejes[0].set_xlabel("desviaciones tipicas respecto a la media")
ejes[0].set_ylabel("densidad")
ejes[0].legend(loc="upper right")
ejes[0].set_ylim(0, 0.47)
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

# --- Derecha: la cola en escala logaritmica. La ruina no esta en el centro, esta al fondo.
ejes[1].plot(x, normal, color=AZUL, linewidth=1.8)
ejes[1].plot(x, cola, color=ROJO, linewidth=1.6, linestyle="--")
ejes[1].axvline(corte, color=TEXTO, linewidth=0.8, alpha=0.5)
ejes[1].set_yscale("log")
ejes[1].set_ylim(1e-6, 0.6)
ejes[1].set_xlim(0, 8)
ejes[1].annotate("la linea marca donde la t\npesa más que la normal",
                 xy=(corte, 4e-3), xytext=(0.15, 2.0e-3), color=TEXTO, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9,
                                 connectionstyle="arc3,rad=-0.25"))
ejes[1].annotate("en z = 3 la t tiene 4 veces más masa;\nen z = 4, casi 60 veces: el cuarto\nmomento lo mide, la varianza no",
                 xy=(4.7, 1.2e-4), xytext=(0.9, 2.0e-6), color=ROJO, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
ejes[1].set_title("La cola en escala logarítmica: la t manda al fondo")
ejes[1].set_xlabel("desviaciones tipicas respecto a la media")
ejes[1].set_ylabel("densidad (escala logaritmica)")
ejes[1].tick_params(axis="y", which="minor", left=False)
numeros(ejes[1], ejes="x")

guardar(fig, "momentos-misma-varianza-distinta-curtosis")
