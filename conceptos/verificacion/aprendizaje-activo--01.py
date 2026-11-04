import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = make_moons(n_samples=100, noise=0.25, random_state=0)

def precision_al_etiquetar(estrategia, semilla):
    rng = np.random.default_rng(semilla)
    idx = np.arange(len(y))
    rng.shuffle(idx)                        # el orden de llegada de los datos es aleatorio
    etiquetados = [int(i) for i in idx[:4]]
    sin_etiquetar = [int(i) for i in idx[4:]]
    modelo = LogisticRegression(max_iter=1000)

    while len(etiquetados) < 12:            # presupuesto: 12 etiquetas en total
        # Se reentrena con lo etiquetado hasta ahora: la incertidumbre se mide con este modelo
        modelo.fit(X[etiquetados], y[etiquetados])
        if estrategia == "aleatorio":
            # choice con size=1 devuelve un array de un elemento: de ahi el [0]
            elegido = int(rng.choice(sin_etiquetar, size=1, replace=False)[0])
        else:
            # Incertidumbre: la probabilidad mas cercana a 0,5 esta en la frontera
            # [:, 1] es la columna de la clase positiva; con [:, 0] se elegiria lo contrario
            p = modelo.predict_proba(X[sin_etiquetar])[:, 1]
            elegido = sin_etiquetar[int(np.argmin(np.abs(p - 0.5)))]
        etiquetados.append(elegido)
        sin_etiquetar.remove(elegido)       # remove borra por valor y recorre la lista entera

    modelo.fit(X[etiquetados], y[etiquetados])
    return accuracy_score(y, modelo.predict(X))

for est in ("aleatorio", "incertidumbre"):
    puntuaciones = [precision_al_etiquetar(est, s) for s in range(5)]
    print(f"{est:>14}: accuracy con 12 etiquetas = {np.mean(puntuaciones):.3f}")
# ->      aleatorio: accuracy con 12 etiquetas = 0.776
# -> incertidumbre: accuracy con 12 etiquetas = 0.850
