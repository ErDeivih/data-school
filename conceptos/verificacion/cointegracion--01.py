import numpy as np
from statsmodels.tsa.stattools import coint

rng = np.random.default_rng(7)
n = 250
x = np.cumsum(rng.normal(0, 1, n)) + 100          # paseo aleatorio: I(1)
z = np.zeros(n)
for t in range(1, n):                             # desvio estacionario AR(1)
    z[t] = 0.85 * z[t - 1] + rng.normal(0, 0.5)
y = 2.0 * x + 5 + z                               # I(1) pero atado a x

beta = np.polyfit(x, y, 1)[0]
residuo = y - beta * x
rho = np.polyfit(residuo[:-1], np.diff(residuo), 1)[0]   # raiz del residuo, estilo Dickey-Fuller
t_eg, p_eg, _ = coint(y, x)

print(f"beta estimada por MCO   {beta:.3f}")        # -> 2.033
print(f"raiz del residuo (DF)   {rho:.3f}")         # -> -0.239
print(f"Engle-Granger  t {t_eg:.3f}  p {p_eg:.4f}")  # -> Engle-Granger  t -5.814  p 0.0000

x2 = np.cumsum(rng.normal(0, 1, n)) + 100
y2 = np.cumsum(rng.normal(0, 1, n)) + 200         # paseo independiente: sin relacion
t2, p2, _ = coint(y2, x2)
print(f"par sin relacion  t {t2:.3f}  p {p2:.4f}")   # -> par sin relacion  t -1.752  p 0.6525
print(f"beta espuria        {np.polyfit(x2, y2, 1)[0]:.3f}")   # -> 0.899
