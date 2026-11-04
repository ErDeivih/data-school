import numpy as np
from scipy import stats

# Chequeo de SRM: esperaba 50/50 y llego esto. Hay que investigar antes de leer la metrica.
observado = np.array([10180, 9820])
esperado = np.array([10000, 10000])
chi2, p = stats.chisquare(observado, esperado)

print(f"chi2 {chi2:.2f}  p {p:.4f}")                        # -> chi2 6.48  p 0.0109
print(f"proporcion observada {observado[0] / observado.sum():.4f}")
# -> proporcion observada 0.5090
