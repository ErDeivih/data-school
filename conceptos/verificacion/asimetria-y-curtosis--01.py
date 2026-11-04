import numpy as np
from scipy import stats

simetrico = np.array([2, 3, 4, 5, 6, 7, 8], dtype=float)
con_extremo = np.array([1, 1, 1, 2, 2, 3, 5, 9, 20], dtype=float)
# 19 dias planos y un dia de panico: el patron tipico de los retornos reales
retornos = np.array([0.004] * 19 + [-0.08])

# bias=False aplica la correccion de sesgo: es lo mismo que pandas .skew() y .kurt()
print("simetrico", round(float(stats.skew(simetrico, bias=False)), 4),
      round(float(stats.kurtosis(simetrico, bias=False)), 4))         # -> 0.0 -1.2
print("extremo  ", round(float(stats.skew(con_extremo, bias=False)), 4),
      round(float(stats.kurtosis(con_extremo, bias=False)), 4))       # -> 2.1817 4.8761
print("retornos ", round(float(stats.skew(retornos, bias=False)), 4),
      round(float(stats.kurtosis(retornos, bias=False)), 4))          # -> -4.4721 20.0
