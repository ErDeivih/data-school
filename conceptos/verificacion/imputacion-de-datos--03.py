import numpy as np
from sklearn.impute import KNNImputer

# Dos grupos de valores muy separados; la fila con el hueco esta en el grupo bajo.
X = np.array([[1.0, 10.0], [2.0, 12.0], [3.0, np.nan], [8.0, 90.0], [9.0, 95.0]])

# KNN usa los dos vecinos mas parecidos (10 y 12), no la media de toda la columna.
imputado = KNNImputer(n_neighbors=2).fit_transform(X)[2, 1]
print(f"imputado por KNN {imputado:.1f}")            # -> 11.0
print(f"media global     {np.nanmean(X[:, 1]):.1f}")  # -> 51.8
