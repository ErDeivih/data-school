import numpy as np
from sklearn.svm import SVC

# El margen se ve a mano: w=(2,0), b=-5 deja los tres puntos justo en el borde.
X = np.array([[2.0, 3.0], [2.0, 1.0], [3.0, 3.0]])
y = np.array([-1, -1, 1])

for C in (1e6, 0.05):
    m = SVC(kernel="linear", C=C).fit(X, y)
    w = m.coef_[0]
    print(f"C={C:<9g} w=({w[0]:+.2f},{w[1]:+.2f}) b={m.intercept_[0]:+.2f} "
          f"margen={2 / np.linalg.norm(w):.2f} soporte={[int(i) for i in m.support_]}")
    print("   valores de decision:", np.round(m.decision_function(X), 2))
# -> C=1e+06     w=(+2.00,+0.00) b=-5.00 margen=1.00 soporte=[0, 1, 2]
# ->    valores de decision: [-1. -1.  1.]
# -> C=0.05      w=(+0.05,+0.00) b=-1.10 margen=40.00 soporte=[0, 1, 2]
# ->    valores de decision: [-1.   -1.   -0.95]
