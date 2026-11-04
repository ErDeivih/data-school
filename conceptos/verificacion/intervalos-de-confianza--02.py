import numpy as np
from scipy import stats

# Una sola muestra: el intervalo no es un intervalo de probabilidad
datos = np.array([5.2, 4.8, 6.1, 5.5, 4.9, 5.8, 5.0, 6.3])
n = datos.size
media, desv = datos.mean(), datos.std(ddof=1)
error_tipico = desv / np.sqrt(n)
t = stats.t.ppf(0.975, df=n - 1)          # cuantil 97,5 % de una t con 7 gl

print(f"media           {media:.3f}")       # -> 5.450
print(f"error tipico    {error_tipico:.3f}")  # -> 0.201
print(f"t critico       {t:.3f}")            # -> 2.365
print(f"IC 95 %         [{media - t * error_tipico:.3f}, {media + t * error_tipico:.3f}]")  # -> [4.975, 5.925]
