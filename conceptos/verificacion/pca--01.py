import numpy as np

# Seis observaciones de dos variables que se mueven casi juntas.
x = np.array([1.0, 2, 3, 4, 5, 6])
y = np.array([2.0, 3, 5, 4, 6, 7])
X = np.column_stack([x, y])
Xc = X - X.mean(axis=0)                     # centrar: PCA mide dispersion, no posicion

# Matriz de covarianzas con n-1: cada variable consigo misma y con la otra.
S = Xc.T @ Xc / (X.shape[0] - 1)
print("covarianzas:", np.round(S, 2).ravel().tolist())   # -> [3.5, 3.3, 3.3, 3.5]

valores, vectores = np.linalg.eigh(S)       # eigh: solo matrices simetricas, y sin ordenar
orden = np.argsort(valores)[::-1]           # de mayor a menor varianza
valores, vectores = valores[orden], vectores[:, orden]
print("varianza por componente:", np.round(valores, 4).tolist())     # -> [6.8, 0.2]
print("proporcion explicada:", np.round(valores / valores.sum(), 3).tolist())  # -> [0.971, 0.029]
print("direccion de PC1:", np.round(vectores[:, 0], 3).tolist())     # -> [0.707, 0.707]

puntuaciones = Xc @ vectores                # una columna por componente: aun estan las dos
print("proyeccion sobre PC1:", np.round(puntuaciones[:, 0], 2).tolist())
# -> [-3.54, -2.12, 0.0, 0.0, 2.12, 3.54]
