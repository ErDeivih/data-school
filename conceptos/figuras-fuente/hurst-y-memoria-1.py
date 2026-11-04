"""hurst-y-memoria-1.py — por qué la pendiente de log-varianza contra log-retardo ES H.

Izquierda: una nube de puntos por serie, la varianza de los incrementos en cada retardo, en
escala logaritmica. La recta del paseo aleatorio tiene pendiente 1; la persistente sube más
(H mayor) y la que revierte sube menos (H menor). Derecha: la misma pendiente llevada a 10
periodos, para ver que el mismo horizonte da tres dispersiones muy distintas.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 20000
lags = np.array([1, 2, 4, 8, 16, 32, 64])


def hurst_agregada(x, lags):
    """H por regresión log-log de la varianza de los incrementos agregados."""
    var = np.array([np.var(x[l:] - x[:-l], ddof=1) for l in lags])
    pendiente = np.polyfit(np.log(lags), np.log(var), 1)[0]
    return pendiente / 2.0, var


# Tres series con la MISMA varianza a un periodo: solo cambia la memoria de los incrementos.
pasos = azar.normal(0, 1, n)
ar_pos = np.zeros(n)                     # incrementos con memoria positiva (persistencia)
ar_neg = np.zeros(n)                     # incrementos que alternan signo (antipersistencia)
for t in range(1, n):
    ar_pos[t] = 0.4 * ar_pos[t - 1] + pasos[t]
    ar_neg[t] = -0.4 * ar_neg[t - 1] + pasos[t]

series = [
    ("persistente (incrementos con memoria)", ar_pos.cumsum(), ROJO),
    ("paseo aleatorio (incrementos independientes)", pasos.cumsum(), AZUL),
    ("revierte (los incrementos se cancelan)", ar_neg.cumsum(), VERDE),
]

fig, ejes = plt.subplots(1, 2, figsize=(9.8, 4.4), width_ratios=[1.45, 1.0])

estimaciones = [(etiqueta, *hurst_agregada(serie, lags), color)
                for etiqueta, serie, color in series]

# Referencia de pendiente 1 (H = 0,50 exacto), anclada a la varianza del paseo en τ = 8.
var_paseo = estimaciones[1][2]
ejes[0].plot(lags, var_paseo[3] * (lags / lags[3]), color=REJILLA, linewidth=1.4,
             linestyle=":", label="referencia H = 0,50 (pendiente 1)")

for etiqueta, h, var, color in estimaciones:
    ejes[0].plot(lags, var, "o-", color=color, linewidth=1.6, markersize=4.5,
                 label=f"{etiqueta.split(' (')[0]}: H = {h:.2f}")

ejes[0].set_xscale("log")
ejes[0].set_yscale("log")
anotar(ejes[0], "pendiente mayor que 1:\ncrece más que el tiempo",
       xy=(32, estimaciones[0][2][5]), xytext=(0.98, 0.14), color=ROJO, align="right")
anotar(ejes[0], "pendiente menor que 1:\nlos incrementos se cancelan",
       xy=(64, estimaciones[2][2][6]), xytext=(0.36, 0.06), color=VERDE)
titulo(ejes[0], "La varianza crece como τ elevado a 2H",
       "cada punto es la varianza de los incrementos a ese retardo; la pendiente es 2H")
ejes[0].set_xlabel("retardo τ en periodos (escala logarítmica)")
ejes[0].set_ylabel("varianza de los incrementos")
ejes[0].legend(loc="upper left", fontsize=8)
ejes[0].set_ylim(top=estimaciones[0][2].max() * 3.2)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: la misma pendiente llevada a 10 periodos --------------------------------------
tau = 10
alturas = [var[0] * tau ** (2 * h) for _e, h, var, _c in estimaciones]
colores = [c for _e, _h, _v, c in estimaciones]
etiquetas = [f"H = {h:.2f}" for _e, h, _v, _c in estimaciones]
barras = ejes[1].bar(etiquetas, alturas, color=colores, width=0.62, alpha=0.85)
for barra, altura in zip(barras, alturas):
    ejes[1].text(barra.get_x() + barra.get_width() / 2, altura + 0.4, f"{altura:.0f}×",
                 ha="center", color=TEXTO, fontsize=10)
titulo(ejes[1], "La misma cuenta vista a 10 periodos",
       "con la varianza a un periodo igual a 1 en las tres series")
ejes[1].set_ylabel("varianza a 10 periodos (veces la de 1 periodo)")
ejes[1].set_ylim(0, max(alturas) * 1.22)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "hurst-pendiente-log-varianza")
