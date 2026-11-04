import numpy as np
from sklearn.preprocessing import RobustScaler, StandardScaler

x = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [100.0]])

# StandardScaler usa la desviacion poblacional (ddof=0); comprime el grupo normal.
print("standard", np.round(StandardScaler().fit_transform(x).ravel(), 2).tolist())
# -> [-0.5, -0.47, -0.45, -0.42, -0.39, 2.23]

# RobustScaler usa mediana e IQR: no lo mueve el extremo y mantiene separado el grupo.
print("robust  ", np.round(RobustScaler().fit_transform(x).ravel(), 2).tolist())
# -> [-1.0, -0.6, -0.2, 0.2, 0.6, 38.6]
