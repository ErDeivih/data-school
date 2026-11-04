import numpy as np
from scipy import stats

# Cuanto cuesta demostrar equivalencia: manda el margen, y el coste va como 1/margen^2.
def n_por_grupo(margen, sd=1.5, alpha=0.05, potencia=0.80, delta=0.0):
    za, zb = stats.norm.ppf(1 - alpha), stats.norm.ppf(potencia)
    return 2 * sd**2 * (za + zb) ** 2 / (margen - abs(delta)) ** 2

for margen in (0.5, 0.4, 0.3, 0.2):
    print(f"margen {margen:.1f}  n por grupo {np.ceil(n_por_grupo(margen)):.0f}")
# -> margen 0.5  n por grupo 112
# -> margen 0.4  n por grupo 174
# -> margen 0.3  n por grupo 310
# -> margen 0.2  n por grupo 696

# Si la diferencia real no es cero, el estudio se encarece: se pierde margen util.
print(f"con margen 0,3 y una diferencia real de 0,1 hacen falta "
      f"{np.ceil(n_por_grupo(0.3, delta=0.1)):.0f} por grupo")
# -> con margen 0,3 y una diferencia real de 0,1 hacen falta 696 por grupo
print(f"con la formula de superioridad para la misma diferencia de 0,1: "
      f"{np.ceil(2 * 1.5**2 * (stats.norm.ppf(0.95) + stats.norm.ppf(0.80))**2 / 0.1**2):.0f} por grupo")
# -> con la formula de superioridad para la misma diferencia de 0,1: 2783 por grupo
