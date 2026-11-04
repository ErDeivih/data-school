import numpy as np
from scipy import stats

sigma, delta, alpha = 8.0, 2.0, 0.05     # desviacion conocida y efecto que importa
z_alfa = stats.norm.ppf(1 - alpha / 2)    # 1,96 para el 5 % bilateral

def potencia(n):
    # Separacion entre la nula y la alternativa, medida en errores tipicos
    return stats.norm.cdf(delta * np.sqrt(n) / sigma - z_alfa)

def muestra_necesaria(potencia_objetivo):
    z_beta = stats.norm.ppf(potencia_objetivo)
    return int(np.ceil((z_alfa + z_beta) ** 2 * sigma**2 / delta**2))

for n in (25, 126):
    print(f"n = {n:>3}  potencia {potencia(n):.3f}")
# -> n =  25  potencia 0.239
# -> n = 126  potencia 0.801

print(f"n para potencia 0,80: {muestra_necesaria(0.80)}")   # -> 126
print(f"n para potencia 0,90: {muestra_necesaria(0.90)}")   # -> 169
