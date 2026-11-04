import numpy as np

def adf_stat(y, p=1, tendencia=False):
    """Estadistico t del coeficiente de y_{t-1} en la regresion de Dickey-Fuller."""
    dy = np.diff(y)
    X, objetivo = [], []
    for j in range(p, dy.size):
        fila = [y[j]]                                   # y_{t-1}
        if tendencia:
            fila.append(j + 1)                          # tendencia determinista
        fila.append(1.0)                                # constante
        fila += [dy[j - i] for i in range(1, p + 1)]    # retardos de la diferencia
        X.append(fila)
        objetivo.append(dy[j])
    X, d = np.array(X), np.array(objetivo)
    b, *_ = np.linalg.lstsq(X, d, rcond=None)
    resid = d - X @ b
    s2 = resid @ resid / (X.shape[0] - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    return b[0] / np.sqrt(cov[0, 0])

def kpss_stat(y, tendencia=False):
    """Estadistico LM: suma acumulada de residuos sobre la varianza de largo plazo."""
    T = y.size
    X = np.column_stack([np.ones(T), np.arange(1, T + 1)]) if tendencia else np.ones((T, 1))
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    S = np.cumsum(e)
    nlags = int(4 * (T / 100) ** 0.25)                  # regla de Schwert
    s2 = (e @ e) / T
    for l in range(1, nlags + 1):
        s2 += 2 * (1 - l / (nlags + 1)) * (e[l:] @ e[:-l]) / T
    return (S @ S) / (T ** 2 * s2)

rng = np.random.default_rng(0)
n = 300
ruido = rng.normal(0, 1, n)
paseo = np.cumsum(ruido)
print("criticos ADF (constante): -3.43 (1%)  -2.86 (5%)  -2.57 (10%)")
print("criticos KPSS (nivel):     0.739 (1%)   0.463 (5%)   0.347 (10%)")
for nombre, s in (("paseo aleatorio", paseo), ("ruido blanco", ruido)):
    print(f"{nombre:>16}  ADF {adf_stat(s):+.2f}   KPSS {kpss_stat(s):.3f}")
# -> paseo aleatorio: ADF -0.81 y KPSS 1.450
# -> ruido blanco:    ADF -11.78 y KPSS 0.279
