import numpy as np

rng = np.random.default_rng(1)
n = 600
x = np.zeros(n)                       # deriva persistente: lo que captura el momentum
for t in range(1, n):
    x[t] = 0.85 * x[t - 1] + rng.normal(0, 0.012)
u = rng.normal(0, 0.02, n)
rebote = u.copy()
rebote[1:] -= 2.0 * u[:-1]            # reversion de corto plazo, exagerada a proposito
r = x + rebote

futuro = r[12:]
ult12 = np.array([r[i - 12:i].sum() for i in range(12, n)])
ult1 = r[11:-1]

print("corr(12 meses, mes siguiente)   %+.3f" % np.corrcoef(ult12, futuro)[0, 1])
print("corr(ultimo mes, mes siguiente) %+.3f" % np.corrcoef(ult1, futuro)[0, 1])
# -> corr(12 meses, mes siguiente)   +0.125
# -> corr(ultimo mes, mes siguiente) -0.219
