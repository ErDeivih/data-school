import numpy as np
from scipy import stats

# Residuos estandarizados: donde esta la diferencia que el p-valor global no senala.
tabla = np.array([[40, 160], [60, 140]])
chi2, p, gl, esperado = stats.chi2_contingency(tabla, correction=False)
residuos = (tabla - esperado) / np.sqrt(esperado)

print(f"movil       {residuos[0, 0]:+.2f}")   # -> movil       -1.41
print(f"escritorio  {residuos[1, 0]:+.2f}")   # -> escritorio  +1.41
print(f"Yates:      {stats.chi2_contingency(tabla, correction=True)[1]:.4f}")  # -> Yates:      0.0282
