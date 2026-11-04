import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(0)
X = rng.uniform(-3, 3, size=(200, 1))
y = np.sin(X[:, 0]) + rng.normal(scale=0.2, size=200)

F = np.full(y.shape, y.mean())      # arranque: la constante que minimiza el error cuadratico
for _ in range(50):
    residuo = y - F                 # con perdida cuadratica el gradiente negativo es el residuo
    h = DecisionTreeRegressor(max_depth=1, random_state=0).fit(X, residuo)
    F = F + 0.1 * h.predict(X)      # 0,1 es la tasa de aprendizaje

print(f"RMSE final        {np.sqrt(((y - F) ** 2).mean()):.3f}")
print(f"RMSE de la media  {np.sqrt(((y - y.mean()) ** 2).mean()):.3f}")
# -> RMSE final        0.262
# -> RMSE de la media  0.723
