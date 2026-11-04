"""diagnostico-de-residuos-2.py — el caso que Ljung-Box no ve: ruido blanco en la media con la
volatilidad agrupada. El residuo es impredecible; su cuadrado, no."""

import numpy as np

from comun import *

import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch

estilo()


def acf(x, nlags):
    """Autocorrelaciones muestrales con denominador n, la versión sesgada."""
    d = x - x.mean()
    g0 = (d @ d) / d.size
    return np.array([1.0] + [(d[k:] @ d[:-k]) / d.size / g0 for k in range(1, nlags + 1)])


n = 400
azar = np.random.default_rng(4)
z = azar.normal(0, 1, n)
s2 = np.ones(n)
for t in range(1, n):                       # GARCH(1,1): la varianza de hoy copia la de ayer
    s2[t] = 0.3 + 0.5 * s2[t - 1] + 0.4 * z[t - 1] ** 2
r = sm.tsa.ARIMA(np.sqrt(s2) * z, order=(1, 0, 0)).fit().resid

banda = 1.96 / np.sqrt(r.size)
retardos = np.arange(1, 13)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3))

eje = ejes[0]
eje.plot(r, color=AZUL, linewidth=0.8)
eje.set_title("Ruido blanco en la media, no en la varianza")
eje.set_xlabel("instante")
eje.set_ylabel("residuo")
anotar(eje, "rachas de temblor y rachas tranquilas:\nLjung-Box no las ve (p = 0,662)",
       (0, 0), (0.03, 0.90), color=AZUL, flecha=False)
rejilla(eje)
numeros(eje)

eje = ejes[1]
a = acf(r ** 2, 12)
eje.bar(retardos, a[1:], color=ROJO, width=0.6)
eje.axhline(0, color=TEXTO, linewidth=0.9)
for signo in (1, -1):
    eje.axhline(signo * banda, color=MORADO, linewidth=1.0, linestyle="--")
eje.set_title("La varianza de hoy copia la de ayer")
eje.set_xlabel("retardo k de los residuos al cuadrado")
eje.set_xticks(retardos)
anotar(eje, "el retardo 1 vale 0,234 y la banda 0,098:\nARCH-LM p = 4e-06",
       (1, a[1]), (0.30, 0.90), color=ROJO)
rejilla(eje)
numeros(eje)

guardar(fig, "diagnostico-de-residuos-volatilidad")
print("LB %.3f  JB %.2e  ARCH %.2e  acf2_1 %.3f  banda %.3f" % (
    float(acorr_ljungbox(r, lags=[10])["lb_pvalue"].iloc[0]),
    float(stats.jarque_bera(r).pvalue),
    float(het_arch(r, nlags=5, result_object=False)[1]),
    acf(r ** 2, 1)[1], banda))
