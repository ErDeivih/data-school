import numpy as np
from scipy import stats

mu = np.array([0.0, 0.0])
S = np.array([[4.0, 4.2], [4.2, 9.0]])          # varianzas 4 y 9, covarianza 4,2
d = stats.multivariate_normal(mean=mu, cov=S)

print(f"det {np.linalg.det(S):.2f}  rho {S[0, 1] / np.sqrt(S[0, 0] * S[1, 1]):.2f}")
# -> det 18.36  rho 0.70
for x in ([0.0, 0.0], [2.0, 3.0], [4.0, 6.0]):
    m2 = float(np.array(x) @ np.linalg.inv(S) @ np.array(x))   # Mahalanobis al cuadrado
    print(f"{x}  mahalanobis2 {m2:.3f}  densidad {d.pdf(x):.6f}")
# -> [0.0, 0.0]  mahalanobis2 0.000  densidad 0.037144
# -> [2.0, 3.0]  mahalanobis2 1.176  densidad 0.020626
# -> [4.0, 6.0]  mahalanobis2 4.706  densidad 0.003532
