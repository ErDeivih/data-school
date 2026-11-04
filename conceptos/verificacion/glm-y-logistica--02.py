import numpy as np

# 100 casos: el modelo da 0,8 a los 30 positivos y 0,3 a los 70 negativos.
y = np.array([1.0] * 30 + [0.0] * 70)
p = np.concatenate([np.full(30, 0.8), np.full(70, 0.3)])

# Log-verosimilitud de Bernoulli: suma de y*log(p) + (1-y)*log(1-p).
ll = (y * np.log(p) + (1 - y) * np.log(1 - p)).sum()
base = y.mean()
ll_base = (y * np.log(base) + (1 - y) * np.log(1 - base)).sum()

print(f"log-verosimilitud modelo {ll:.3f}")
print(f"log-verosimilitud base   {ll_base:.3f}")
print(f"2*(ll - ll_base)         {2 * (ll - ll_base):.3f}")
# -> log-verosimilitud modelo -31.662
# -> log-verosimilitud base   -61.086
# -> 2*(ll - ll_base)         58.850
