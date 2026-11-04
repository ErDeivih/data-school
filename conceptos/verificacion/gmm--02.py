import numpy as np

rng = np.random.default_rng(0)
X = np.concatenate([rng.normal(0, 1, 70), rng.normal(5, 1, 70), rng.normal(10, 1, 70)])

def em_1d(x, k, iters=200):
    """Mezcla de k gaussianas en una dimension: devuelve la log-verosimilitud y los parametros."""
    # arranque: k centros repartidos uniformemente por el rango de los datos.
    mu = np.linspace(x.min(), x.max(), k)
    var = np.full(k, x.var())
    pi = np.full(k, 1 / k)
    for _ in range(iters):
        d = pi * np.exp(-(x[:, None] - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)
        # keepdims=True conserva la forma (n,1) y la division se emite por filas.
        r = d / d.sum(axis=1, keepdims=True)
        nk = r.sum(axis=0)
        pi = nk / x.size
        mu = (r * x[:, None]).sum(axis=0) / nk
        var = (r * (x[:, None] - mu) ** 2).sum(axis=0) / nk
    return np.log(d.sum(axis=1)).sum(), mu, var, pi

for k in range(1, 6):
    ll, mu, var, pi = em_1d(X, k)
    q = 3 * k - 1                              # media, varianza y peso por grupo, menos 1
    print(f"k={k}  log-verosimilitud {ll:8.1f}  BIC {-2 * ll + q * np.log(X.size):8.1f}")
# -> k=1  log-verosimilitud   -594.9  BIC   1200.4
# -> k=2  log-verosimilitud   -556.9  BIC   1140.5
# -> k=3  log-verosimilitud   -517.0  BIC   1076.8
# -> k=4  log-verosimilitud   -517.0  BIC   1092.9
# -> k=5  log-verosimilitud   -515.3  BIC   1105.5

ll, mu, var, pi = em_1d(X, 3)
punto = np.array([2.5])
d = pi * np.exp(-(punto[:, None] - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)
print("medias ordenadas:", np.round(np.sort(mu), 2).tolist())          # -> [0.11, 5.11, 9.9]
print("pertenencia ordenada del punto 2.5:", np.round(np.sort((d / d.sum()).ravel()), 3).tolist())
# -> [0.0, 0.41, 0.59]
