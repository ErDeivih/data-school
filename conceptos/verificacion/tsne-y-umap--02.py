import numpy as np

# Cuatro puntos de un tetraedro regular: los seis pares distan exactamente lo mismo.
vertices = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) * 10
D = np.linalg.norm(vertices[:, None, :] - vertices[None, :, :], axis=2)   # los None dan los ejes

# La mejor proyeccion lineal a dos dimensiones: las dos primeras componentes principales.
centrado = vertices - vertices.mean(axis=0)
vectores = np.linalg.eigh(centrado.T @ centrado)[1][:, ::-1][:, :2]
plano = centrado @ vectores
D2 = np.linalg.norm(plano[:, None, :] - plano[None, :, :], axis=2)

print("distancias desde el primer vertice, original:", np.round(D[0, 1:], 2).tolist())
# -> [28.28, 28.28, 28.28]
print("las mismas distancias en el plano:", np.round(D2[0, 1:], 2).tolist())
# -> [28.28, 20.0, 20.0]
print("cociente mayor/menor original:", round(float(D[D > 0].max() / D[D > 0].min()), 2))
# -> 1.0
print("cociente mayor/menor en el plano:", round(float(D2[D2 > 0].max() / D2[D2 > 0].min()), 2))
# -> 1.41
