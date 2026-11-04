import numpy as np

def pnl_reversion(x, ventana=60, entrada=2.0, salida=0.0, stop=3.5):
    """Compra cuando el z-score es muy negativo y vende cuando es muy positivo."""
    pos, pnl, ops = 0, 0.0, 0
    for t in range(ventana, len(x) - 1):
        v = x[t - ventana:t]
        z = (x[t] - v.mean()) / v.std(ddof=1)
        if pos == 0:
            if z > entrada:
                pos, ops = -1, ops + 1
            elif z < -entrada:
                pos, ops = 1, ops + 1
        elif pos == 1 and (z >= salida or z <= -stop):
            pos = 0
        elif pos == -1 and (z <= salida or z >= stop):
            pos = 0
        pnl += pos * (x[t + 1] - x[t])
    return pnl, ops

rng = np.random.default_rng(0)
n = 2000
rev = np.zeros(n)                       # serie que revierte: AR(1) con rho 0,95
for t in range(1, n):
    rev[t] = 0.95 * rev[t - 1] + rng.normal(0, 0.01)
paseo = np.cumsum(rng.normal(0, 0.01, n))   # serie que pasea: sin nivel al que volver

for nombre, serie in (("revierte", rev), ("pasea", paseo)):
    p, ops = pnl_reversion(serie)
    print("%-8s pnl %+7.4f  operaciones %3d  pnl/operacion %+.5f" % (nombre, p, ops, p / max(ops, 1)))
# -> revierte pnl +1.1429  operaciones  43  pnl/operacion +0.02658
# -> pasea    pnl +0.0870  operaciones  36  pnl/operacion +0.00242
