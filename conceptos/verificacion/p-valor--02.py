import numpy as np
from scipy import stats

rng = np.random.default_rng(0)
reps, n = 5000, 30

# Bajo H0 (los dos grupos salen de la misma normal) el p-valor es uniforme:
# con 5000 contrastes, alrededor del 5 % dan p < 0,05 sin que exista ningun efecto.
a = rng.normal(0, 1, size=(reps, n))
b = rng.normal(0, 1, size=(reps, n))
p_nulo = stats.ttest_ind(a, b, axis=1).pvalue

# Bajo H1 (media 0,5 mas alta) los p-valores se apiñan cerca de cero
c = rng.normal(0.5, 1, size=(reps, n))
p_real = stats.ttest_ind(c, b, axis=1).pvalue

print(f"P(p < 0,05) sin efecto:  {np.mean(p_nulo < 0.05):.3f}")   # -> 0.051
print(f"P(p < 0,10) sin efecto:  {np.mean(p_nulo < 0.10):.3f}")   # -> 0.105
print(f"P(p < 0,05) con efecto:  {np.mean(p_real < 0.05):.3f}")   # -> 0.475
