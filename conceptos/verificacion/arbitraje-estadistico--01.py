import numpy as np

rng = np.random.default_rng(0)
T, N, K = 600, 12, 2
F = rng.normal(0, 0.01, (T, K))                                    # dos factores comunes
B = np.column_stack([rng.normal(0.9, 0.2, N),
                     np.r_[np.full(6, -0.6), np.full(6, 0.6)]])    # exposiciones

# Lo que revierte es el PRECIO del residuo (una desviacion acumulada), no su retorno
X = np.zeros((T, N))
for t in range(1, T):
    X[t] = 0.92 * X[t - 1] + rng.normal(0, 0.003, N)
dX = np.diff(X, axis=0, prepend=np.zeros((1, N)))
R = F @ B.T + dX

ventana = 60
pesos = np.zeros((T, N))
for t in range(ventana, T - 1):
    X_reg = np.column_stack([np.ones(ventana), F[t - ventana:t]])
    beta = np.linalg.lstsq(X_reg, R[t - ventana:t], rcond=None)[0][1:]
    resid = R[t - ventana:t] - F[t - ventana:t] @ beta     # retorno del residuo
    nivel = np.cumsum(resid, axis=0)                       # nivel acumulado del residuo
    s = (nivel[-1] - nivel.mean(axis=0)) / nivel.std(axis=0, ddof=1)
    w = -np.clip(s, -3.0, 3.0)                             # apostamos contra la desviacion
    w = w / np.abs(w).sum()
    pesos[t] = w - w.mean()                                # neutralidad en dolares

usados = np.arange(ventana, T - 1)
bruto = np.array([pesos[t] @ R[t + 1] for t in usados])
giro = np.abs(np.diff(pesos[usados], axis=0)).sum(axis=1)
coste = giro * 0.0005

print("suma de pesos neta      %+.6f" % pesos[usados].sum(axis=1).mean())
print("exposicion bruta         %.4f" % np.abs(pesos[usados]).sum(axis=1).mean())
print("beta neta al factor 1   %+.3f" % (pesos[usados] @ B[:, 0]).mean())
print("pnl bruto acumulado    %+.4f" % bruto.sum())
print("giro medio por periodo   %.3f" % giro.mean())
print("coste acumulado (5 pb)  %+.4f" % coste.sum())
print("pnl neto de costes     %+.4f" % (bruto.sum() - coste.sum()))
print("coste de equilibrio     %.2f pb por unidad de giro" % (1e4 * bruto.sum() / giro.sum()))
# -> suma de pesos neta      +0.000000
# -> exposicion bruta         0.9435
# -> beta neta al factor 1   +0.006
# -> pnl bruto acumulado    +0.1765
# -> giro medio por periodo   0.433
# -> coste acumulado (5 pb)  +0.1165
# -> pnl neto de costes     +0.0600
# -> coste de equilibrio     7.58 pb por unidad de giro
