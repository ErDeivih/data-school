import numpy as np

# Vida media del diferencial: cuanto tarda en recorrer la mitad del camino de vuelta
rng = np.random.default_rng(3)
n = 400
z = np.zeros(n)
for t in range(1, n):
    z[t] = 0.9 * z[t - 1] + rng.normal(0, 1)

phi = np.polyfit(z[:-1], z[1:], 1)[0]
print(f"phi estimado          {phi:.4f}")                    # -> 0.8917
print(f"vida media (periodos) {-np.log(2) / np.log(phi):.2f}")  # -> 6.05
