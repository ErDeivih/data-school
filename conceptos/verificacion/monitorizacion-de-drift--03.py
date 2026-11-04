import numpy as np
from scipy import stats

# El p-valor del KS no dice si la diferencia importa: depende sobre todo del tamano.
rng = np.random.default_rng(11)
for n in (50, 5000, 200000):
    referencia = rng.normal(0.0, 1.0, size=n)
    actual = rng.normal(0.2, 1.0, size=n)   # mismo desplazamiento en los tres casos
    ks = stats.ks_2samp(referencia, actual)
    print(f"n={n:>6}  KS {ks.statistic:.3f}  p {ks.pvalue:.4f}")
