import numpy as np

rng = np.random.default_rng(4)
n = 48
t = np.arange(n)
estacional = np.tile([4.0, 0.0, -3.0, -1.0], 12)      # patron trimestral fijo
y = 50 + 0.5 * t + estacional + rng.normal(0, 1.2, n)

def descomposicion(y, m):
    """Clasica: tendencia por media movil centrada de orden m y estacional por fases."""
    tend = np.full(y.size, np.nan)
    pesos = np.concatenate([[0.5], np.ones(m - 1), [0.5]]) / m
    for i in range(y.size - m):
        tend[i + m // 2] = pesos @ y[i:i + m + 1]
    detrend = y - tend
    fase = np.array([np.nanmean(detrend[k::m]) for k in range(m)])
    est = np.tile(fase - fase.mean(), y.size // m + 1)[:y.size]
    return tend, est, y - tend - est

tend, est, resid = descomposicion(y, 4)
print("estacional por trimestre", np.round(est[:4], 2))     # -> [ 3.73 -0.09 -3.1  -0.54]
print("tendencia en el punto 10 y en el 40", np.round([tend[9], tend[39]], 2))  # -> [54.42 69.4 ]
print("desv del residuo %.2f  (el ruido simulado era 1.20)" % np.nanstd(resid[3:-3], ddof=1))  # -> 1.09
vr = np.nanvar(resid[3:-3])
print("fuerza estacional %.2f" % max(0, 1 - vr / np.nanvar((est + resid)[3:-3])))   # -> 0.84
print("fuerza de tendencia %.2f" % max(0, 1 - vr / np.nanvar((tend + resid)[3:-3])))  # -> 0.97
