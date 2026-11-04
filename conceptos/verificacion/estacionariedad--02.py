import numpy as np

# 2000 caminos de 400 pasos: comparamos como crece la dispersion con el tiempo
rng = np.random.default_rng(0)
n, m = 400, 2000
pasos = rng.normal(0, 1, (m, n))
paseo = np.cumsum(pasos, axis=1)            # y_t = y_{t-1} + eps_t: raiz unitaria
ar1 = np.zeros((m, n))                      # AR(1) con phi = 0.8: estacionario
for t in range(1, n):
    ar1[:, t] = 0.8 * ar1[:, t - 1] + pasos[:, t]

for nombre, x in (("paseo aleatorio", paseo), ("AR(1) phi=0.8", ar1)):
    print(f"{nombre:>16}  desv en t=50 {x[:, 49].std(ddof=1):5.2f}"
          f"   t=200 {x[:, 199].std(ddof=1):5.2f}   t=400 {x[:, 399].std(ddof=1):5.2f}")
# -> paseo aleatorio: 7.16, 14.15 y 20.20 (crece como la raiz de t)
# -> AR(1) phi=0.8:  1.65,  1.67 y  1.64 (constante: 1/sqrt(1-0.64) = 1.67)
