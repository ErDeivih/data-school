import numpy as np

# El error típico del Sharpe: por qué 12 meses no bastan para presumir.
# Aproximación de Lo (2002): SE ≈ sqrt((1 + Sharpe²/2) / n)
def error_tipico_sharpe(retornos, rf=0.0):
    exceso = retornos - rf
    sr = exceso.mean() / exceso.std(ddof=1)
    return sr, np.sqrt((1 + sr**2 / 2) / exceso.size)

rng = np.random.default_rng(0)

# Misma estrategia "real" (Sharpe mensual 0,1), medida con 12 y con 240 meses
for n in (12, 60, 240):
    sr, se = error_tipico_sharpe(rng.normal(0.003, 0.03, size=n))
    print(f"n={n:>4}  Sharpe mensual {sr:+.2f}  error tipico ±{se:.2f}  anual {sr*np.sqrt(12):+.2f}")
