import warnings

import numpy as np
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.stats.stattools import durbin_watson

# statsmodels avisa de un cambio de API futuro en het_arch; la salida se lee mejor sin el aviso.
warnings.filterwarnings("ignore", category=FutureWarning)

azar = np.random.default_rng(11)
n = 400
y = np.zeros(n)
for t in range(1, n):                       # AR(1) con phi = 0,7
    y[t] = 0.7 * y[t - 1] + azar.normal(0, 1)

r = sm.tsa.ARIMA(y, order=(1, 0, 0)).fit().resid
rho1 = sm.tsa.acf(r, nlags=1)[1]
print("Ljung-Box h=10 p", round(float(acorr_ljungbox(r, lags=[10])["lb_pvalue"].iloc[0]), 3))
# -> Ljung-Box h=10 p 0.729
print("Jarque-Bera p", round(float(stats.jarque_bera(r).pvalue), 3))
# -> Jarque-Bera p 0.239
print("ARCH-LM q=5 p", round(float(het_arch(r, nlags=5, result_object=False)[1]), 3))
# -> ARCH-LM q=5 p 0.997
print("Durbin-Watson", round(float(durbin_watson(r)), 3))       # -> Durbin-Watson 1.938
print("2(1 - rho1)", round(2 * (1 - rho1), 3))                  # -> 2(1 - rho1) 1.938
print("ACF residuos 1..4", np.round(sm.tsa.acf(r, nlags=4)[1:], 3),
      "banda", round(1.96 / np.sqrt(r.size), 3))
# -> ACF residuos 1..4 [ 0.031 -0.044  0.013  0.014] banda 0.098
