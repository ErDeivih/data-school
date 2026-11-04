import numpy as np
from sklearn.cluster import KMeans

# K-means corta por rectas: con dos anillos concentricos parte cada anillo en dos.
rng = np.random.default_rng(0)
theta = rng.uniform(0, 2 * np.pi, 400)
radio = np.concatenate([rng.normal(1.0, 0.08, 200), rng.normal(3.0, 0.08, 200)])
X = np.column_stack([radio * np.cos(theta), radio * np.sin(theta)])

for k in (2, 3):
    # fit_predict es fit mas predict y devuelve las etiquetas directamente.
    etiquetas = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
    # Cuanto del anillo interior (los 200 primeros puntos) cae en un solo grupo.
    # max sobre las dos hipotesis porque el numero de grupo es arbitrario.
    acuerdo = max((etiquetas[:200] == 0).mean(), (etiquetas[:200] == 1).mean())
    print(f"k={k}: el anillo interior cae en un unico grupo el {acuerdo:.0%} de las veces")
# -> k=2: el anillo interior cae en un unico grupo el 53% de las veces
# -> k=3: el anillo interior cae en un unico grupo el 34% de las veces
