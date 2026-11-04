import numpy as np

# Correlacion cero NO implica independencia: Y = X^2 con X simetrica.
X = np.array([-1.0, 0.0, 1.0])
Y = X**2

cov = float(np.mean((X - X.mean()) * (Y - Y.mean())))
corr = float(np.corrcoef(X, Y)[0, 1])

print("X            ", X.tolist())              # salida: [-1.0, 0.0, 1.0]
print("Y = X^2      ", Y.tolist())              # salida: [1.0, 0.0, 1.0]
print("covarianza   ", round(cov, 4))           # salida: 0.0
print("correlacion  ", round(corr, 4))          # salida: 0.0
print("pero Y depende de X:", bool(np.allclose(Y, X**2)))  # salida: True
