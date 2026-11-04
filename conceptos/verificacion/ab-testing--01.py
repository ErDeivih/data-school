import numpy as np
from scipy import stats

# Cuantas unidades hacen falta para detectar un punto porcentual sobre una base del 12 %.
p0, mde, alfa, potencia = 0.12, 0.01, 0.05, 0.80
z_a = stats.norm.ppf(1 - alfa / 2)
z_b = stats.norm.ppf(potencia)
n = 2 * (z_a + z_b) ** 2 * p0 * (1 - p0) / mde ** 2

print(f"z_alfa {z_a:.3f}  z_beta {z_b:.3f}")     # -> z_alfa 1.960  z_beta 0.842
print(f"n por rama {n:.0f}")                     # -> n por rama 16577
print(f"dias a 2000 visitas/dia {2 * n / 2000:.1f}")  # -> dias a 2000 visitas/dia 16.6
