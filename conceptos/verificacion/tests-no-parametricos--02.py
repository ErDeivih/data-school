import numpy as np
from scipy import stats

# Doce pares antes/despues: once mejoran un poco y uno empeora muchisimo.
antes = np.array([210, 195, 230, 205, 220, 200, 215, 225, 199, 231, 208, 222], float)
cambios = np.array([-8, -6, -7, -9, -5, -8, -6, -7, -9, -5, -6, 30], float)

tp, p_t = stats.ttest_rel(antes, antes + cambios)
w, p_w = stats.wilcoxon(antes, antes + cambios)

print(f"t apareado  {tp:+.2f}  p {p_t:.4f}")   # -> t apareado  +1.24  p 0.2422
print(f"Wilcoxon    W {w:.1f}  p {p_w:.4f}")  # -> Wilcoxon    W 12.0  p 0.0342
print(f"mejoran {(cambios < 0).sum()} de {cambios.size}")  # -> mejoran 11 de 12
