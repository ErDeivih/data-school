import numpy as np
from sklearn.cluster import KMeans

# Los centroides se mueven hasta que las asignaciones dejan de cambiar.
# reshape(-1, 1) convierte los 6 numeros en una matriz de 6 filas y 1 columna:
# sklearn espera siempre una matriz de observaciones x variables.
X = np.array([1, 2, 3, 10, 11, 12.0]).reshape(-1, 1)
m = KMeans(n_clusters=2, init=np.array([[1.0], [10.0]]), n_init=1, random_state=0).fit(X)
print("etiquetas:", m.labels_)
# cluster_centers_ tiene forma (2, 1); ravel() lo aplana a un array de 2 numeros.
print("centroides:", np.round(m.cluster_centers_.ravel(), 3))
print("inercia:", round(m.inertia_, 3), " iteraciones:", m.n_iter_)
# -> etiquetas: [0 0 0 1 1 1]
# -> centroides: [ 2. 11.]
# -> inercia: 4.0  iteraciones: 2

# El codo: la inercia baja siempre, la pregunta es donde deja de bajar en serio.
for k in (1, 2, 3, 4):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print(f"k={k}  inercia {km.inertia_:.3f}")
# -> k=1  inercia 125.500
# -> k=2  inercia 4.000
# -> k=3  inercia 2.500
# -> k=4  inercia 1.000
