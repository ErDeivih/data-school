import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score, train_test_split

# Senal debil y mucho ruido: el escenario donde "el mejor de N" engana
X, y = make_regression(n_samples=150, n_features=8, n_informative=2,
                       noise=45.0, random_state=0)

for semilla in (0, 1, 2):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=semilla)
    rng = np.random.default_rng(semilla)
    alphas = 10 ** rng.uniform(-3, 3, size=100)          # 100 configuraciones al azar
    # np.array es lo que permite usar argmax y median despues; una lista no las tiene
    puntuaciones = np.array([cross_val_score(Ridge(alpha=a), X_tr, y_tr, cv=3,
                                             scoring="r2").mean() for a in alphas])
    mejor = int(np.argmax(puntuaciones))
    modelo = Ridge(alpha=alphas[mejor]).fit(X_tr, y_tr)  # se reentrena el ganador para medirlo
    print(f"split {semilla}: CV del ganador {puntuaciones[mejor]:+.3f}"
          f"   R2 en test {modelo.score(X_te, y_te):+.3f}"
          f"   mediana de las 100 {np.median(puntuaciones):+.3f}")
# -> split 0: CV del ganador +0.033   R2 en test +0.166   mediana de las 100 -0.027
# -> split 1: CV del ganador +0.126   R2 en test +0.178   mediana de las 100 +0.097
# -> split 2: CV del ganador +0.040   R2 en test +0.152   mediana de las 100 +0.005
