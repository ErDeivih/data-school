"""momentum-1.py — lo que paga el momentum y lo que duele cuando el rebote llega.

Izquierda: la rentabilidad acumulada del decil ganador y del decil perdedor durante diez anos.
Las dos parten de 1 y se separan: esa separación es la prima del factor, y es lo que cobra la
cartera larga-corta. Derecha: esa cartera mes a mes. Crece, y de vez en cuando se hunde en dos
meses, justo cuando los valores que lleva en corto rebotan con más fuerza.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
meses = 120

# Quintil ganador y quintil perdedor: pequenas diferencias por mes que se acumulan.
ganador = azar.normal(0.008, 0.040, meses)
perdedor = azar.normal(-0.002, 0.050, meses)
acum_ganador = np.cumprod(1 + ganador)
acum_perdedor = np.cumprod(1 + perdedor)

# La cartera larga-corta: la resta de los dos, sobre 180 meses y con tres rebotes violentos.
meses_lc = 180
cartera = ganador.mean() - perdedor.mean() + azar.normal(0, 0.048, meses_lc)
rebotes = [40, 78, 104]
for t in rebotes:
    cartera[t] = -0.09
    cartera[t + 1] = -0.08
acumulado = np.cumprod(1 + cartera)

fig, ejes = plt.subplots(1, 2, figsize=(9.8, 4.3), width_ratios=[1.0, 1.35])

# --- Izquierda: el ganador y el perdedor, acumulados ----------------------------------------
ejes[0].axhline(1.0, color=REJILLA, linewidth=0.9, linestyle=":")
ejes[0].plot(acum_ganador, color=VERDE, linewidth=1.9)
ejes[0].plot(acum_perdedor, color=ROJO, linewidth=1.9)
anotar(ejes[0], f"el decil ganador: {acum_ganador[-1] - 1:+.0%} en diez años",
       xy=(meses - 1, acum_ganador[-1]), xytext=(0.97, 0.72), color=VERDE, align="right")
anotar(ejes[0], f"el decil perdedor: {acum_perdedor[-1] - 1:+.0%}",
       xy=(meses - 1, acum_perdedor[-1]), xytext=(0.97, 0.30), color=ROJO, align="right")
titulo(ejes[0], "Ordenar por la señal 12-1 separa dos mundos",
       "valor de 1 euro en cada decil; la resta de las dos curvas es la prima del factor")
ejes[0].set_xlabel("mes")
ejes[0].set_ylabel("valor de 1 euro")
rejilla(ejes[0])
numeros(ejes[0])

# --- Derecha: la cartera larga-corta y sus tres desplomes ------------------------------------
eje_x = np.arange(meses_lc)
ejes[1].plot(eje_x, acumulado, color=MORADO, linewidth=1.9)
for k, t in enumerate(rebotes):
    ejes[1].axvspan(t - 0.5, t + 4.5, color=ROJO, alpha=0.13)
    caida = acumulado[t + 1] / acumulado[t - 1] - 1
    ejes[1].annotate(f"{caida:.0%} en dos meses:\nlos que iba cortos rebotan",
                     xy=(t + 3, acumulado[t + 3]), xytext=(0.30, 0.96 - 0.21 * k),
                     textcoords="axes fraction", color=ROJO, fontsize=8, va="top",
                     arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
anotar(ejes[1], f"y aun así acaba en {acumulado[-1]:.2f}",
       xy=(meses_lc - 1, acumulado[-1]), xytext=(0.97, 0.30), color=MORADO, align="right")
titulo(ejes[1], "Crece, y de vez en cuando se hunde",
       "cartera larga-corta igual ponderada: valor de 1 euro invertido en el primer mes")
ejes[1].set_xlabel("mes")
ejes[1].set_ylabel("valor de 1 euro")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "momentum-quintiles-y-desplome")
