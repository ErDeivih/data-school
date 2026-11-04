import numpy as np

# Un autoencoder lineal con error cuadratico aprende el mismo subespacio que PCA.
X = np.array([[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0],
              [2.3, 2.7], [2.0, 1.6], [1.0, 1.1], [1.5, 1.6], [1.1, 0.9]])
Xc = X - X.mean(axis=0)
n = X.shape[0]
# full_matrices=False porque solo hacen falta los min(n, d) vectores, no la matriz cuadrada
# completa: con 10 filas y 2 columnas, la version completa devolveria una U de 10x10.
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)

varianza = S ** 2 / (n - 1)                      # ddof=1: estimamos la media
print("varianza por componente:", varianza.round(3).tolist())   # -> [1.284, 0.049]
print("1a componente explica  :", round(float(varianza[0] / varianza.sum()), 3))  # -> 0.963

# Cuello de botella de 1 dimension: proyectar y reconstruir.
# Vt[:1] es la primera componente principal, como una fila de 1 x 2. Al proyectar y volver
# se tira la segunda componente, asi que el error esperado es exactamente su varianza.
rec = (Xc @ Vt[:1].T) @ Vt[:1]
error = float(((Xc - rec) ** 2).sum() / (n - 1))
print("error de reconstruccion:", round(error, 4))    # -> 0.0491
print("varianza descartada    :", round(float(varianza[1]), 4))   # -> 0.0491
