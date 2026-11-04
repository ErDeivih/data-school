import numpy as np
from scipy import stats

# Una cola larga de verdad: cada valor es casi el doble que el anterior.
x = np.array([1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0])
print(f"asimetria original  {stats.skew(x):.2f}")           # -> 1.38
print(f"asimetria con log1p {stats.skew(np.log1p(x)):.2f}")  # -> 0.31

# Box-Cox estima la potencia por maxima verosimilitud; lambda=0 seria el logaritmo.
ajustado, lam = stats.boxcox(x)
print(f"asimetria Box-Cox   {stats.skew(ajustado):.2f}")     # -> 0.04
print(f"lambda estimada     {lam:.2f}")                      # -> -0.07
