import numpy as np

rng = np.random.default_rng(3)
T, N = 300, 80
R = rng.normal(0, 0.02, (T, N))
R[1:] += -0.04 * R[:-1].copy()     # reversion de corto plazo

senal = -R[:-1]                    # lo que sabemos al decidir
futuro = R[1:]                     # retorno del dia siguiente

def ic_por_dia(a, c):
    ra = np.argsort(np.argsort(a, axis=1), axis=1).astype(float)
    rc = np.argsort(np.argsort(c, axis=1), axis=1).astype(float)
    ra -= ra.mean(axis=1, keepdims=True)
    rc -= rc.mean(axis=1, keepdims=True)
    return (ra * rc).sum(axis=1) / np.sqrt((ra ** 2).sum(axis=1) * (rc ** 2).sum(axis=1))

ic = ic_por_dia(senal, futuro)
print("IC medio         %+.4f" % ic.mean())
print("t-stat del IC    %+.2f" % (ic.mean() / (ic.std(ddof=1) / np.sqrt(ic.size))))
print("dias con IC > 0  %.0f%%" % (100 * (ic > 0).mean()))
# -> IC medio         +0.0344
# -> t-stat del IC    +5.60
# -> dias con IC > 0  62%
