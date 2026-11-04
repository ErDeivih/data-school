import numpy as np
from scipy import stats

# El contraste bilateral y el IC del 95 % responden lo mismo:
# se rechaza H0: mu = mu0 justo cuando mu0 se queda fuera del intervalo.
piezas = np.array([5.2, 4.8, 6.1, 5.5, 4.9, 5.8, 5.0, 6.3])
n = piezas.size
error = piezas.std(ddof=1) / np.sqrt(n)
t_crit = stats.t.ppf(0.975, df=n - 1)          # cuantil 97,5 % de una t con 7 gl
bajo, alto = piezas.mean() - t_crit * error, piezas.mean() + t_crit * error

print(f"IC 95 % de la media: [{bajo:.3f}, {alto:.3f}]")   # -> [4.975, 5.925]
for mu0 in (5.5, 6.0):
    p = stats.ttest_1samp(piezas, popmean=mu0).pvalue
    print(f"mu0 = {mu0}  p = {p:.3f}  dentro del IC = {bajo <= mu0 <= alto}")
# -> mu0 = 5.5  p = 0.811  dentro del IC = True
# -> mu0 = 6.0  p = 0.029  dentro del IC = False
