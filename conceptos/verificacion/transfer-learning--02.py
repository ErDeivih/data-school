import numpy as np

rng = np.random.default_rng(0)
w_origen = np.array([1.5, -0.5])      # modelo ya entrenado en la tarea de origen
w_destino = np.array([0.2, 1.8])      # solucion buena para la tarea nueva
X = rng.normal(0, 1, size=(24, 2))
y_origen, y_destino = X @ w_origen, X @ w_destino

print("ancla lambda   error en origen   error en destino")
for lam in (0.0, 0.05, 0.5, 5.0):
    w = w_origen.copy()          # cada lambda parte del mismo punto de origen
    for _ in range(200):
        # El segundo sumando es el gradiente del anclaje L2: lam * (w - w_origen).
        grad = X.T @ (X @ w - y_destino) / len(X) + lam * (w - w_origen)
        w -= 0.1 * grad          # descenso de gradiente con tasa fija
    print(f"{lam:>11}   {np.abs(X @ w - y_origen).mean():14.3f}"
          f"   {np.abs(X @ w - y_destino).mean():15.3f}")
# -> ancla lambda   error en origen   error en destino
# ->         0.0            1.386             0.000
# ->        0.05            1.256             0.136
# ->         0.5            0.687             0.720
# ->         5.0            0.128             1.260
