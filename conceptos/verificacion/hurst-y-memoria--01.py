import numpy as np

def hurst_agregada(x, lags=(1, 2, 4, 8, 16, 32)):
    """H por regresion log-log de la varianza de los incrementos agregados."""
    x = np.asarray(x, float)
    lags = np.asarray(lags)
    var = np.array([np.var(x[l:] - x[:-l], ddof=1) for l in lags])
    return np.polyfit(np.log(lags), np.log(var), 1)[0] / 2

rng = np.random.default_rng(42)
blanco = rng.normal(0, 1, 20000).cumsum()        # paseo aleatorio: H deberia ser 0,5
ret = np.zeros(20000)
for t in range(1, 20000):                        # AR(1) con phi = 0,3: memoria positiva
    ret[t] = 0.3 * ret[t - 1] + rng.normal(0, 1)
persistente = ret.cumsum()

print(f"paseo aleatorio  H = {hurst_agregada(blanco):.3f}")      # -> 0.506
print(f"con memoria AR1  H = {hurst_agregada(persistente):.3f}")  # -> 0.577
