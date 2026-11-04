import numpy as np
from scipy import stats

# La Mahalanobis al cuadrado se comporta como una ji-cuadrado con p grados de libertad.
rng = np.random.default_rng(0)
mu = np.array([0.0, 0.0])
S = np.array([[4.0, 4.2], [4.2, 9.0]])
Sinv = np.linalg.inv(S)

X = rng.multivariate_normal(mu, S, size=200000)
m2 = np.einsum("ij,jk,ik->i", X, Sinv, X)        # una Mahalanobis por fila, sin bucle
corte = stats.chi2.ppf(0.95, df=2)
print(f"P(mahalanobis2 < {corte:.3f})  simulada {(m2 < corte).mean():.3f}  teorica 0.950")
# -> P(mahalanobis2 < 5.991)  simulada 0.950  teorica 0.950
print(f"proporcion de puntos fuera de la elipse del 95 %: {(m2 > corte).mean():.3f}")
# -> proporcion de puntos fuera de la elipse del 95 %: 0.050

# Sumar dos variables correlacionadas NO es sumar sus varianzas.
a = np.ones(2)
print(f"sd de la suma {np.sqrt(a @ S @ a):.4f}  suma de sd {np.sqrt(S[0, 0]) + np.sqrt(S[1, 1]):.4f}")
# -> sd de la suma 4.6260  suma de sd 5.0000
