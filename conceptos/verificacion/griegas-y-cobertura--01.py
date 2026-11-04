import numpy as np

# Dos calls de cobertura: columnas = A y B; filas = gamma y vega por contrato
G = np.array([[2.0, 5.0],
              [10.0, 18.0]])
exposicion = np.array([60.0, 100.0])      # gamma y vega que hay que neutralizar
delats = np.array([0.45, 0.55])           # delta de cada call
delta_cartera = 12.0

w = np.linalg.solve(G, exposicion)

print(f"pesos {w[0]:.2f} {w[1]:.2f}")                                  # -> pesos -41.43 28.57
print(f"gamma cubierta {G[0] @ w:.2f} vega cubierta {G[1] @ w:.2f}")    # -> gamma cubierta 60.00 vega cubierta 100.00
print(f"delta residual {delta_cartera + w @ delats:+.2f}")              # -> delta residual +9.07
print(f"spot {-delta_cartera - w @ delats:+.2f} acciones")              # -> spot -9.07 acciones
print(f"condicion {np.linalg.cond(G):.2f}")                             # -> condicion 32.33