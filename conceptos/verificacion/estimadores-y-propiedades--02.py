import numpy as np

rng = np.random.default_rng(0)

# Dos predictores casi identicos (correlacion 0,99) y 20 observaciones:
# el diseno esta mal condicionado y OLS paga por ello con enorme varianza.
n = 20
z = rng.normal(0, 1, size=n)
X = np.column_stack([z, z + 0.2 * rng.normal(0, 1, size=n)])
X = (X - X.mean(axis=0)) / X.std(axis=0)      # centradas y con suma de cuadrados 1

beta_real = np.array([1.5, -0.8])
XtX = X.T @ X
lam = 0.5

ols, ridge = [], []
for _ in range(2000):
    y = X @ beta_real + rng.normal(0, 1.0, size=n)
    Xty = X.T @ y
    ols.append(np.linalg.solve(XtX, Xty))
    ridge.append(np.linalg.solve(XtX + lam * np.eye(2), Xty))
ols, ridge = np.array(ols), np.array(ridge)

print(f"correlacion entre predictores {np.corrcoef(X[:, 0], X[:, 1])[0, 1]:.2f}")
print(f"OLS    media {np.round(ols.mean(axis=0), 3)}  desv tipica {np.round(ols.std(axis=0), 3)}")
print(f"ridge  media {np.round(ridge.mean(axis=0), 3)}  desv tipica {np.round(ridge.std(axis=0), 3)}")
print(f"OLS    ECM {np.mean(np.sum((ols - beta_real) ** 2, axis=1)):.4f}")
print(f"ridge  ECM {np.mean(np.sum((ridge - beta_real) ** 2, axis=1)):.4f}")
