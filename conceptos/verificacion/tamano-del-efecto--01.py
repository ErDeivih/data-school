import numpy as np
from scipy import stats

# Dos grupos con media 68,4 y 74,6 y desviacion 11,2 exactas: la d no cambia,
# solo cambia cuanta informacion tenemos para demostrarla.
def grupo(n, media, sd):
    z = np.arange(n) - (n - 1) / 2               # simetrico alrededor de cero
    return media + sd * z / np.sqrt((z**2).sum() / (n - 1))

for n in (10, 100):
    control = grupo(n, 68.4, 11.2)
    tratado = grupo(n, 74.6, 11.2)
    sp = np.sqrt((control.var(ddof=1) + tratado.var(ddof=1)) / 2)
    t, p = stats.ttest_ind(tratado, control)
    print(f"n={n:>3}  d={6.2 / sp:.2f}  t={t:+.2f}  p={p:.4f}")
    # -> n= 10  d=0.55  t=+1.24  p=0.2317
    # -> n=100  d=0.55  t=+3.91  p=0.0001
