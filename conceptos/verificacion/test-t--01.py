import numpy as np
from scipy import stats

# Tiempo de atencion (segundos) de 9 llamadas; el manual promete 240 s de media.
tiempos = np.array([231, 245, 238, 226, 250, 242, 235, 228, 244])
t, p = stats.ttest_1samp(tiempos, popmean=240)

print(f"media  {tiempos.mean():.2f}")                             # -> media  237.67
print(f"t {t:.3f}  df {tiempos.size - 1}  p {p:.4f}")            # -> t -0.847  df 8  p 0.4214
