import numpy as np

rng = np.random.default_rng(0)
n, repeticiones, sigma2 = 10, 20000, 4.0

# Dos estimadores de la varianza: dividir por n (sesgado) y por n-1 (insesgado)
m1 = np.empty(repeticiones)
m2 = np.empty(repeticiones)
for i in range(repeticiones):
    muestra = rng.normal(0, np.sqrt(sigma2), size=n)
    m1[i] = muestra.var()             # ddof=0: el MLE, sesgado hacia abajo
    m2[i] = muestra.var(ddof=1)       # ddof=1: el insesgado de Bessel

for nombre, est in (("dividir por n  ", m1), ("dividir por n-1", m2)):
    sesgo = est.mean() - sigma2
    ecm = ((est - sigma2) ** 2).mean()
    print(f"{nombre}  media {est.mean():.3f}  sesgo {sesgo:+.3f}  ECM {ecm:.3f}")
