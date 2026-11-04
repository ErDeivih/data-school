import numpy as np
from scipy import stats

# Filas movil/escritorio, columnas convierte/no convierte.
tabla = np.array([[40, 160],
                  [60, 140]])
chi2, p, gl, esperado = stats.chi2_contingency(tabla, correction=False)

print(esperado.astype(int).tolist())                      # -> [[50, 150], [50, 150]]
print(f"chi2 {chi2:.3f}  gl {gl}  p {p:.4f}")             # -> chi2 5.333  gl 1  p 0.0209
print(f"V de Cramer {np.sqrt(chi2 / tabla.sum()):.3f}")   # -> V de Cramer 0.115
