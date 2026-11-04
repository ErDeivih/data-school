import warnings

import numpy as np
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch

warnings.filterwarnings("ignore", category=FutureWarning)
n = 400

# (1) El modelo se ha dejado fuera una media movil estacional: e_t + 0,6 * e_{t-4}.
azar = np.random.default_rng(11)
e = azar.normal(0, 1, n + 10)
y = np.zeros(n + 10)
for t in range(1, n + 10):
    y[t] = 0.7 * y[t - 1] + e[t] + 0.6 * e[t - 4]
r = sm.tsa.ARIMA(y[10:], order=(1, 0, 0)).fit().resid
print("MA(4) escondida -> Ljung-Box p %.2e" % float(acorr_ljungbox(r, lags=[10])["lb_pvalue"].iloc[0]))
# -> MA(4) escondida -> Ljung-Box p 1.06e-13
print("  ACF de los residuos 1..5", np.round(sm.tsa.acf(r, nlags=5)[1:], 3))
# ->   ACF de los residuos 1..5 [-0.024 -0.135  0.015  0.403 -0.004]
print("  banda del 95%", round(1.96 / np.sqrt(r.size), 3))      # ->   banda del 95% 0.098
print("  ARCH-LM p", round(float(het_arch(r, nlags=5, result_object=False)[1]), 3))
# ->   ARCH-LM p 0.211

# (2) Ruido blanco en la media, pero con la volatilidad agrupada: GARCH(1,1).
azar2 = np.random.default_rng(4)
z = azar2.normal(0, 1, n)
s2 = np.ones(n)
for t in range(1, n):
    s2[t] = 0.3 + 0.5 * s2[t - 1] + 0.4 * z[t - 1] ** 2
r2 = sm.tsa.ARIMA(np.sqrt(s2) * z, order=(1, 0, 0)).fit().resid
print("GARCH escondido -> Ljung-Box p", round(float(acorr_ljungbox(r2, lags=[10])["lb_pvalue"].iloc[0]), 3))
# -> GARCH escondido -> Ljung-Box p 0.662
print("  Jarque-Bera p %.2e" % float(stats.jarque_bera(r2).pvalue))
# ->   Jarque-Bera p 2.65e-03
print("  ARCH-LM p %.2e" % float(het_arch(r2, nlags=5, result_object=False)[1]))
# ->   ARCH-LM p 4.25e-06
print("  ACF de los cuadrados 1..5", np.round(sm.tsa.acf(r2 ** 2, nlags=5)[1:], 3))
# ->   ACF de los cuadrados 1..5 [ 0.234 -0.004 -0.015  0.131  0.002]
