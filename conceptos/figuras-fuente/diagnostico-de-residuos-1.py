"""diagnostico-de-residuos-1.py — la ACF de los residuos: el contraste dice que queda estructura
y el correlograma dice en que retardo esta."""

import numpy as np

from comun import *

import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox

estilo()


def acf(x, nlags):
    """Autocorrelaciones muestrales con denominador n, la versión sesgada."""
    d = x - x.mean()
    g0 = (d @ d) / d.size
    return np.array([1.0] + [(d[k:] @ d[:-k]) / d.size / g0 for k in range(1, nlags + 1)])


n = 400
retardos = np.arange(1, 13)

# Modelo correcto: los datos son un AR(1) y el modelo tambien.
azar = np.random.default_rng(11)
y = np.zeros(n)
for t in range(1, n):
    y[t] = 0.7 * y[t - 1] + azar.normal(0, 1)
r_bueno = sm.tsa.ARIMA(y, order=(1, 0, 0)).fit().resid

# Modelo al que le falta un termino estacional: e_t + 0,6 · e_{t-4}. Cada simulacion lleva su
# propia semilla, para que el resultado no dependa de cuantos numeros haya gastado la anterior.
azar2 = np.random.default_rng(11)
e = azar2.normal(0, 1, n + 10)
y2 = np.zeros(n + 10)
for t in range(1, n + 10):
    y2[t] = 0.7 * y2[t - 1] + e[t] + 0.6 * e[t - 4]
r_malo = sm.tsa.ARIMA(y2[10:], order=(1, 0, 0)).fit().resid

banda = 1.96 / np.sqrt(r_bueno.size)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3), sharey=True)

for eje, r, titulo_panel, color, nota in (
    (ejes[0], r_bueno, "Modelo correcto: residuo sin memoria", AZUL,
     "ni una barra fuera de la banda\nLjung-Box p = 0,729"),
    (ejes[1], r_malo, "Falta el término estacional: pico en el 4", ROJO,
     "la barra del retardo 4 vale 0,403\nLjung-Box p = 1e-13"),
):
    a = acf(r, 12)
    eje.bar(retardos, a[1:], color=color, width=0.6)
    eje.axhline(0, color=TEXTO, linewidth=0.9)
    for signo in (1, -1):
        eje.axhline(signo * banda, color=MORADO, linewidth=1.0, linestyle="--")
    eje.set_title(titulo_panel)
    eje.set_xlabel("retardo k")
    eje.set_xticks(np.arange(2, 13, 2))
    eje.set_ylim(-0.35, 0.55)
    anotar(eje, nota, (retardos[3], a[4]), (0.30, 0.90), color=color, flecha=(color == ROJO))
    rejilla(eje)
    numeros(eje)
ejes[0].set_ylabel("autocorrelación de los residuos")

guardar(fig, "diagnostico-de-residuos-acf")
print("banda %.3f  lag4 bueno %.3f  lag4 malo %.3f" % (banda, acf(r_bueno, 4)[4], acf(r_malo, 4)[4]))
print("p bueno %.3f  p malo %.2e" % (
    float(acorr_ljungbox(r_bueno, lags=[10])["lb_pvalue"].iloc[0]),
    float(acorr_ljungbox(r_malo, lags=[10])["lb_pvalue"].iloc[0])))
