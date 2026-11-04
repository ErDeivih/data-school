import numpy as np

# El mecanismo, no el caso concreto: la probabilidad de seguir vivo baja con el resultado.
rng = np.random.default_rng(0)
n = 2000
resultado = rng.normal(0.02, 0.15, size=n)          # rentabilidad real de cada fondo
# Supervivencia: cuanta peor es la rentabilidad, menos probable es seguir en la base de datos.
prob_vivir = 1.0 / (1.0 + np.exp(-(resultado + 0.02) / 0.05))
vive = rng.random(n) < prob_vivir

print(f"fondos simulados        {n}")                       # -> 2000
print(f"supervivientes          {int(vive.sum())}")          # -> 1178
print(f"media real              {resultado.mean():+.4f}")    # -> +0.0158
print(f"media de supervivientes {resultado[vive].mean():+.4f}")  # -> +0.1027
print(f"sesgo al alza           {resultado[vive].mean() - resultado.mean():+.4f}")  # -> +0.0869
