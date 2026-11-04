import numpy as np

def hurst(x, lags=(2, 4, 8, 16, 32, 64)):
    x = np.asarray(x, float)
    lags = np.asarray(lags)
    var = np.array([np.var(x[l:] - x[:-l], ddof=1) for l in lags])
    return np.polyfit(np.log(lags), np.log(var), 1)[0] / 2

rng = np.random.default_rng(0)
# Diez paseos aleatorios puros (H real = 0,500) de solo 250 observaciones cada uno
estimaciones = [hurst(rng.normal(0, 1, 250).cumsum()) for _ in range(10)]

print("H estimada en cada muestra:")
print(np.round(estimaciones, 3))
print(f"minimo {min(estimaciones):.3f}  maximo {max(estimaciones):.3f}")  # -> minimo 0.253  maximo 0.558
print(f"media  {np.mean(estimaciones):.3f}")                              # -> 0.440
