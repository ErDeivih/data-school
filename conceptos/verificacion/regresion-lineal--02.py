import numpy as np

x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([4.0, 5.0, 6.0, 8.0, 9.0])

# Version matricial: la primera columna de unos es el intercepto.
X = np.column_stack([np.ones_like(x), x])
beta = np.linalg.solve(X.T @ X, X.T @ y)      # ecuaciones normales
print("beta (b0, b1):", np.round(beta, 3))

# Los residuos son ortogonales a las columnas de X; de ahi salen las ecuaciones normales.
residuos = y - X @ beta
print("X^T e:", np.round(X.T @ residuos, 12) + 0.0)
print(f"media de y {y.mean():.3f}  media de las predicciones {(X @ beta).mean():.3f}")
# -> beta (b0, b1): [2.5 1.3]
# -> X^T e: [0. 0.]
# -> media de y 6.400  media de las predicciones 6.400
