import numpy as np

# Filas: estado de origen. Columnas: estado de destino. La ultima fila es absorbente.
P = np.array([[0.90, 0.08, 0.02],
              [0.20, 0.60, 0.20],
              [0.00, 0.00, 1.00]])

P12 = np.linalg.matrix_power(P, 12)
Q = P[:2, :2]                       # transiciones entre estados transitorios
N = np.linalg.inv(np.eye(2) - Q)    # matriz fundamental

print(f"al dia a 12 meses {P12[0, 0]:.4f}")        # -> al dia a 12 meses 0.4545
print(f"impago a 12 meses {P12[0, 2]:.4f}")        # -> impago a 12 meses 0.4406
print(f"meses hasta impago {N[0].sum():.2f}")      # -> meses hasta impago 20.00
print(f"filas suman {P.sum(axis=1)}")               # -> filas suman [1. 1. 1.]