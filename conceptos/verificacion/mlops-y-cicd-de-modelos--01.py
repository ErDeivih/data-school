# El ruido de la medicion: mismo codigo, mismos datos, distinta semilla de particion.
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

X, y = make_regression(n_samples=300, n_features=6, noise=15.0, random_state=7)

for semilla in (0, 1, 2):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=semilla)
    mae = mean_absolute_error(y_te, Ridge(alpha=1.0).fit(X_tr, y_tr).predict(X_te))
    print(f"semilla {semilla}: MAE {mae:.2f}")
# -> semilla 0: MAE 13.86
# -> semilla 1: MAE 13.43
# -> semilla 2: MAE 12.23
