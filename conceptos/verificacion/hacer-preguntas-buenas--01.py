import numpy as np
from scipy.stats import norm

# Datos de ejemplo: pedidos entregados en 48 h o menos, por mes.
p1, n1 = 0.78, 12_000     # febrero
p2, n2 = 0.85, 11_400     # marzo

diferencia = p2 - p1
ee_intervalo = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)   # sin agrupar

# Para contrastar la igualdad de proporciones se usa la proporcion agrupada,
# que es mas conservadora que el error tipico del intervalo.
p_comun = (n1 * p1 + n2 * p2) / (n1 + n2)
ee_test = np.sqrt(p_comun * (1 - p_comun) * (1 / n1 + 1 / n2))
z = diferencia / ee_test

print(f"diferencia        {diferencia:+.3f}  ({diferencia * 100:+.1f} puntos)")
print(f"error tipico (IC) {ee_intervalo:.5f}")                  # -> 0.00505
print(f"z del contraste   {z:.2f}")                             # -> 13.76
print(f"p-valor (2 colas) {2 * norm.sf(abs(z)):.1e}")           # -> 4.6e-43
print(f"diferencia / ee   {diferencia / ee_intervalo:.1f}")     # -> 13.9: no es ruido
