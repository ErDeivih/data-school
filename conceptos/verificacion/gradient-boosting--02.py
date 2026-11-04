import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
X = rng.uniform(-3, 3, size=(240, 2))
y = np.sin(X[:, 0]) + 0.5 * X[:, 1] + rng.normal(scale=0.2, size=240)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

for lr in (0.05, 0.3, 1.0):
    m = GradientBoostingRegressor(n_estimators=60, learning_rate=lr,
                                  max_depth=2, random_state=0).fit(X_tr, y_tr)
    rmse_tr = np.sqrt(((y_tr - m.predict(X_tr)) ** 2).mean())
    rmse_te = np.sqrt(((y_te - m.predict(X_te)) ** 2).mean())
    print(f"lr={lr:<4} train {rmse_tr:.3f}  test {rmse_te:.3f}")
# -> lr=0.05 train 0.286  test 0.327
# -> lr=0.3  train 0.109  test 0.245
# -> lr=1.0  train 0.038  test 0.458
