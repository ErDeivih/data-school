import numpy as np
from sklearn.feature_selection import VarianceThreshold

# Cuatro columnas: una constante, dos identicas y una informativa.
X = np.array([[1.0, 3.0, 5.0, 5.0],
              [2.0, 3.0, 4.0, 4.0],
              [3.0, 3.0, 3.0, 3.0],
              [4.0, 3.0, 2.0, 2.0]])

# threshold=0.0 tira solo las constantes; no detecta la redundancia entre columnas.
sel = VarianceThreshold(threshold=0.0).fit(X)
print("conservadas:", sel.get_support().tolist())   # -> [True, False, True, True]
print(f"correlacion columnas 3 y 4 {np.corrcoef(X[:, 2], X[:, 3])[0, 1]:.2f}")   # -> 1.00
