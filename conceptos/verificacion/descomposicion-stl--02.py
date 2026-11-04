import numpy as np

rng = np.random.default_rng(5)
n = 48
t = np.arange(n)
tendencia = 100 * np.exp(0.01 * t)                    # crece un 1% por periodo
factor = np.tile([1.10, 0.95, 0.90, 1.05], 12)        # estacionalidad multiplicativa
y = tendencia * factor * np.exp(rng.normal(0, 0.02, n))

def patron_estacional(serie, m=4):
    """Media por fase de la serie sin tendencia (media movil centrada de orden m)."""
    pesos = np.concatenate([[0.5], np.ones(m - 1), [0.5]]) / m
    tend = np.full(serie.size, np.nan)
    for i in range(serie.size - m):
        tend[i + m // 2] = pesos @ serie[i:i + m + 1]
    detrend = serie - tend
    return np.array([np.nanmean(detrend[k::m]) for k in range(m)])

fase = patron_estacional(y)
print("amplitud en crudo       %.1f" % (fase.max() - fase.min()))       # -> 26.4
fase_log = patron_estacional(np.log(y))
print("amplitud en logaritmos  %.3f" % (fase_log.max() - fase_log.min()))  # -> 0.210
print("factores recuperados", np.round(np.exp(fase_log - fase_log.mean()), 3))
# -> [1.106 0.962 0.897 1.048] frente a los simulados 1.10, 0.95, 0.90 y 1.05
