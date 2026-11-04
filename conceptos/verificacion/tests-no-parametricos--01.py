import numpy as np
from scipy import stats

# A tiene valores tipicos mas bajos, pero un unico valor extremo destroza su varianza.
a = np.array([1, 2, 3, 4, 5, 6, 7, 100])
b = np.array([20, 21, 22, 23, 24, 25, 26, 27])

t, p_t = stats.ttest_ind(a, b, equal_var=False)
u, p_u = stats.mannwhitneyu(a, b, alternative="two-sided")

print(f"t de Welch {t:+.2f}  p {p_t:.4f}")   # -> t de Welch -0.62  p 0.5533
print(f"U {u:.1f}  p exacta {p_u:.4f}")     # -> U 8.0  p exacta 0.0104

# Probabilidad de superioridad y desplazamiento de Hodges-Lehmann.
pares = (b[:, None] - a[None, :]).ravel()
print(f"P(B > A) {(b[:, None] > a[None, :]).mean():.3f}")   # -> P(B > A) 0.875
print(f"desplazamiento {np.median(pares):+.1f}")            # -> desplazamiento +19.0
