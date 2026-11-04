import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import jarque_bera

rng = np.random.default_rng(1)
n = 200
x = rng.uniform(1, 10, size=n)
y = 2 + 0.8 * x + rng.normal(0, 0.3 * x)     # error normal, pero de varianza creciente

X = sm.add_constant(x)
ajuste = sm.OLS(y, X).fit()

bp = het_breuschpagan(ajuste.resid, X)       # H0: varianza constante
jb = jarque_bera(ajuste.resid)               # H0: residuos normales
print(f"Breusch-Pagan p {bp[1]:.6f}")
print(f"Jarque-Bera  p {jb[1]:.4f}")
print(f"correlacion de los residuos con x: {np.corrcoef(ajuste.resid, x)[0, 1]:+.3f}")
# -> Breusch-Pagan p 0.000007
# -> Jarque-Bera  p 0.0000
# -> correlacion de los residuos con x: +0.000
