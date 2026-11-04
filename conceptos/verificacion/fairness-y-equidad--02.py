import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

# Mismo modelo en los dos grupos; lo unico que cambia es la prevalencia real.
mu_pos, mu_neg, sd = 0.75, 0.35, 0.15
pi_a, pi_b = 0.30, 0.12


def seleccion(umbral, pi):
    tpr = 1.0 - norm.cdf((umbral - mu_pos) / sd)      # exhaustividad del grupo
    fpr = 1.0 - norm.cdf((umbral - mu_neg) / sd)      # falsas alarmas del grupo
    return pi * tpr + (1.0 - pi) * fpr


# Objetivo de paridad demografica: la misma tasa de seleccion en los dos grupos.
objetivo = 0.5 * (seleccion(0.50, pi_a) + seleccion(0.50, pi_b))
u_a = brentq(lambda u: seleccion(u, pi_a) - objetivo, 0.0, 1.0)
u_b = brentq(lambda u: seleccion(u, pi_b) - objetivo, 0.0, 1.0)
exhaustividad = lambda u: 1.0 - norm.cdf((u - mu_pos) / sd)

print(f"objetivo {objetivo:.3f}  umbral A {u_a:.2f}  umbral B {u_b:.2f}")
print(f"exhaustividad A {exhaustividad(u_a):.3f}  B {exhaustividad(u_b):.3f}")
# -> objetivo 0.325  umbral A 0.56  umbral B 0.46
# -> exhaustividad A 0.897  B 0.974
