import numpy as np
from scipy import stats

# Bondad de ajuste: 200 pedidos en 4 franjas horarias, hipotesis de reparto uniforme.
observado = np.array([40, 60, 70, 30])
esperado = np.array([50, 50, 50, 50])
chi2, p = stats.chisquare(observado, esperado)

print(f"chi2 {chi2:.1f}  gl {observado.size - 1}  p {p:.4f}")
# -> chi2 20.0  gl 3  p 0.0002
