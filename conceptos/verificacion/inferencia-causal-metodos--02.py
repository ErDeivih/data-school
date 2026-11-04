import numpy as np

rng = np.random.default_rng(0)
n = 4000
u = rng.normal(0, 1, n)                             # confusor: motivacion no observada
t = (u + rng.normal(0, 0.5, n) > 0).astype(float)   # el tratamiento depende de u
y = 2.0 * t + 3.0 * u + rng.normal(0, 0.5, n)       # efecto causal real: 2,0

ingenuo = y[t == 1].mean() - y[t == 0].mean()
# Aqui u SI se observa (es una simulacion); en la vida real no lo tendrias
diseno = np.column_stack([np.ones(n), t, u])
ajustado = np.linalg.lstsq(diseno, y, rcond=None)[0][1]

print(f"diferencia cruda      {ingenuo:.2f}")     # -> 6.32
print(f"controlando por u     {ajustado:.2f}")    # -> 2.01
