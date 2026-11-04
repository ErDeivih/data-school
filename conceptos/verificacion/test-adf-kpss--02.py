import numpy as np

# (se repiten adf_stat y kpss_stat del bloque anterior)
def adf_stat(y, p=1, tendencia=False):
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
    T = y.size
    X = np.column_stack([np.ones(T), np.arange(1, T + 1)]) if tendencia else np.ones((T, 1))
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    S = np.cumsum(e)
    nlags = int(4 * (T / 100) ** 0.25)
    s2 = (e @ e) / T
    for l in range(1, nlags + 1):
        s2 += 2 * (1 - l / (nlags + 1)) * (e[l:] @ e[:-l]) / T
    return (S @ S) / (T ** 2 * s2)

rng = np.random.default_rng(3)
n = 300
t = np.arange(n)
series = {
    "ruido": rng.normal(0, 1, n),
    "paseo": np.cumsum(rng.normal(0, 1, n)),
    "paseo con deriva": np.cumsum(rng.normal(0.1, 1, n)),
    "tendencia + ruido": 0.1 * t + rng.normal(0, 1, n),
}
for nombre, s in series.items():
    print(f"{nombre:>17}  ADF {adf_stat(s):+.2f}   KPSS {kpss_stat(s):.3f}")
# -> ruido -12.05 / 0.166;  paseo -0.22 / 4.750;  paseo con deriva -2.69 / 1.768
# -> tendencia + ruido -0.55 / 5.092 (los dos se equivocan por omitir la tendencia)

s = series["tendencia + ruido"]
print("con tendencia en el contraste: ADF %+.2f  KPSS %.3f"
      % (adf_stat(s, tendencia=True), kpss_stat(s, tendencia=True)))
# -> ADF -12.83 y KPSS 0.029: estacionaria alrededor de la tendencia
