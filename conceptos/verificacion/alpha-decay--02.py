import numpy as np

rng = np.random.default_rng(12)
T, N = 1200, 60
s = rng.normal(0, 1, (T, N))
b = np.where(np.arange(T) < 700, 0.001, 0.0)[:, None]     # el alpha muere en t = 700
r = b * s + rng.normal(0, 0.02, (T, N))

def ic_por_dia(a, c):
    ra = np.argsort(np.argsort(a, axis=1), axis=1).astype(float)
    rc = np.argsort(np.argsort(c, axis=1), axis=1).astype(float)
    ra -= ra.mean(axis=1, keepdims=True)
    rc -= rc.mean(axis=1, keepdims=True)
    return (ra * rc).sum(axis=1) / np.sqrt((ra ** 2).sum(axis=1) * (rc ** 2).sum(axis=1))

# La senal se conoce al empezar el periodo y el retorno se cobra en ese mismo periodo
ic = ic_por_dia(s, r)
print("IC medio antes del corte %+.4f" % ic[:700].mean())
print("IC medio despues         %+.4f" % ic[700:].mean())
print("IC medio ultimos 200     %+.4f" % ic[-200:].mean())
print("diferencia antes-despues %+.4f" % (ic[:700].mean() - ic[700:].mean()))
# -> IC medio antes del corte +0.0514
# -> IC medio despues         -0.0046
# -> IC medio ultimos 200     -0.0078
# -> diferencia antes-despues +0.0560
