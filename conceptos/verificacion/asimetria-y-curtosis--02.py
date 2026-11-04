import numpy as np
from scipy import stats

# Con pocos datos, la asimetria muestral de una normal ya se mueve muchisimo
rng = np.random.default_rng(0)

v20 = np.array([stats.skew(rng.normal(size=20), bias=False) for _ in range(2000)])
v200 = np.array([stats.skew(rng.normal(size=200), bias=False) for _ in range(2000)])
v2000 = np.array([stats.skew(rng.normal(size=2000), bias=False) for _ in range(2000)])

print(f"n   20: entre {v20.min():+.2f} y {v20.max():+.2f}")      # -> n   20: entre -2.01 y +2.04
print(f"n  200: entre {v200.min():+.2f} y {v200.max():+.2f}")    # -> n  200: entre -0.58 y +0.59
print(f"n 2000: entre {v2000.min():+.2f} y {v2000.max():+.2f}")  # -> n 2000: entre -0.19 y +0.18

retornos = np.array([0.004] * 19 + [-0.08])
print("ejemplo:", round(float(stats.skew(retornos, bias=False)), 2))   # -> -4.47
