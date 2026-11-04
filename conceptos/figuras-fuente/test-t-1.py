"""test-t-1.py — los mismos ocho empleados medidos antes y después: analizados como datos
apareados (t ≈ 14) o como dos grupos independientes (t ≈ 1,4). Figura de la página del
test t."""

import numpy as np
from scipy import stats

from comun import *

estilo()

antes = np.array([210, 195, 230, 205, 220, 200, 215, 225], float)
despues = np.array([200, 188, 219, 197, 214, 191, 208, 216], float)
diferencias = antes - despues                     # +8,375 s de media
n = antes.size

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.1))

# --- Izquierda: cada persona es su propio control y la caida se repite en las ocho.
for i in range(n):
    ejes[0].plot([0, 1], [antes[i], despues[i]], color=CIAN, linewidth=1.2, alpha=0.85)
ejes[0].plot([0, 1], [antes.mean(), despues.mean()], color=ROJO, linewidth=2.6, zorder=3)
ejes[0].plot([0, 1], [antes.mean(), despues.mean()], "o", color=ROJO, markersize=6, zorder=4)
anotar(ejes[0], "cada persona baja entre 6 y 11 s:\nla caída se repite en las ocho",
       xy=(0.5, 205), xytext=(0.05, 0.91), color=CIAN)
anotar(ejes[0], "la media baja 8,4 s", xy=(0.55, 208), xytext=(0.34, 0.72), color=ROJO)
ejes[0].text(0.02, 0.03, "entre personas hay 12 s de diferencia; esa variabilidad se cancela al restar",
             transform=ejes[0].transAxes, fontsize=8.5, color=TEXTO)
ejes[0].set_xticks([0, 1])
ejes[0].set_xticklabels(["antes", "después"])
ejes[0].set_xlim(-0.25, 1.25)
ejes[0].set_ylim(180, 240)
ejes[0].set_ylabel("segundos por llamada atendida")
titulo(ejes[0], "Cada persona es su propio control",
       "lo que se contrasta son las ocho diferencias, no los dos grupos por separado")
rejilla(ejes[0])

# --- Derecha: la misma diferencia, con el error típico de cada forma de analizarla.
t_pareado = stats.ttest_rel(antes, despues).statistic
t_indep = stats.ttest_ind(antes, despues, equal_var=False).statistic
ee_pareado = diferencias.std(ddof=1) / np.sqrt(n)
ee_indep = np.sqrt(antes.var(ddof=1) / n + despues.var(ddof=1) / n)
tc_pareado = stats.t.ppf(0.975, n - 1)
tc_indep = stats.t.ppf(0.975, 13.98)
filas = [(1.0, ee_pareado, tc_pareado, VERDE, "apareado: t = " + f"{t_pareado:+.2f}".replace(".", ",")),
         (0.0, ee_indep, tc_indep, ROJO, "independiente: t = " + f"{t_indep:+.2f}".replace(".", ","))]
for y, ee, tc, color, etiqueta in filas:
    ejes[1].plot([diferencias.mean() - tc * ee, diferencias.mean() + tc * ee], [y, y],
                 color=color, linewidth=2.6)
    ejes[1].plot([diferencias.mean()], [y], "o", color=color, markersize=8, zorder=3)
    ejes[1].text(diferencias.mean() + tc * ee + 0.6, y, etiqueta, fontsize=9, color=color,
                 va="center")
ejes[1].axvline(0, color=TEXTO, linewidth=1.2)
anotar(ejes[1], "el cero queda fuera:\np ≈ 0,000002", xy=(7.4, 0.88), xytext=(0.03, 0.86),
       color=VERDE)
anotar(ejes[1], "el cero queda dentro:\np = 0,19", xy=(0, 0.06), xytext=(0.03, 0.24),
       color=ROJO)
ejes[1].set_xlabel("diferencia antes − después (segundos)")
ejes[1].set_xlim(-10, 34)
ejes[1].set_ylim(-0.7, 1.7)
ejes[1].set_yticks([])
titulo(ejes[1], "La misma diferencia, dos conclusiones",
       "el error típico de 0,60 s frente al de 6,01 s: ahí está toda la diferencia")
rejilla(ejes[1], eje="x")
numeros(ejes[1], ejes="x")

guardar(fig, "test-t-pareado-frente-a-independiente")
