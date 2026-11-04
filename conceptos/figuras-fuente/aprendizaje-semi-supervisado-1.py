"""aprendizaje-semi-supervisado-1.py — con doce etiquetas, la frontera que sale de una recta
no separa nada; la propagación de etiquetas aprovecha la posición de los 150 puntos y
reconstruye la frontera curva. Figura de la página de aprendizaje semisupervisado (fase 6)."""

import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.semi_supervised import LabelSpreading

from comun import *

estilo()

# Dos lunas entrelazadas, como en el ejemplo de la página: la clase no se separa con una
# recta, así que la geometría de los puntos sin etiquetar es información de verdad.
X, y = make_moons(n_samples=200, noise=0.2, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)

# -1 significa "sin etiquetar": es la convención de scikit-learn para el semisupervisado.
y_parcial = np.full_like(y_tr, -1)
etiquetados = np.array([0, 1, 2, 3, 40, 41, 42, 43, 80, 81, 82, 83])
y_parcial[etiquetados] = y_tr[etiquetados]        # 12 etiquetas de 150 filas

recta = LogisticRegression(max_iter=1000).fit(X_tr[etiquetados], y_tr[etiquetados])
propaga = LabelSpreading(kernel="knn", n_neighbors=7).fit(X_tr, y_parcial)
nota_recta = float(recta.score(X_te, y_te))
nota_propaga = float(propaga.score(X_te, y_te))

# Rejilla para pintar la frontera de cada modelo sobre todo el plano. Se deja poco margen
# alrededor de los datos: lejos de los puntos, un grafo de vecinos extrapola sin sentido.
paso = 0.02
xx, yy = np.meshgrid(np.arange(X[:, 0].min() - 0.15, X[:, 0].max() + 0.15, paso),
                     np.arange(X[:, 1].min() - 0.15, X[:, 1].max() + 0.15, paso))
malla = np.c_[xx.ravel(), yy.ravel()]

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.6))

for ax, modelo, nota, corto, largo, pos in (
        (ejes[0], recta, nota_recta, "Doce etiquetas y una frontera recta",
         "regresión logística con las 12 filas etiquetadas", (0.03, 0.10)),
        (ejes[1], propaga, nota_propaga, "La geometría de los 150 puntos sí separa",
         "propagación de etiquetas sobre 7 vecinos", (0.97, 0.10))):
    # El fondo son las dos zonas que el modelo asigna a cada clase, en un tono muy claro para
    # que los puntos se lean por encima.
    prob = modelo.predict_proba(malla)[:, 1].reshape(xx.shape)
    ax.contourf(xx, yy, prob, levels=[0, 0.5, 1], colors=[AZUL, ROJO], alpha=0.12, zorder=0)
    ax.contour(xx, yy, prob, levels=[0.5], colors=[TEXTO], linewidths=1.1, zorder=2)
    # Todos los puntos de entrenamiento, con su clase verdadera, para que se vea la forma.
    ax.scatter(X_tr[y_tr == 0, 0], X_tr[y_tr == 0, 1], color=AZUL, s=18, alpha=0.45,
               linewidths=0, zorder=3)
    ax.scatter(X_tr[y_tr == 1, 0], X_tr[y_tr == 1, 1], color=ROJO, s=18, alpha=0.45,
               linewidths=0, zorder=3)
    # Las 12 etiquetas de verdad, marcadas con borde negro: es lo único que ve la recta.
    ax.scatter(X_tr[etiquetados][y_tr[etiquetados] == 0, 0],
               X_tr[etiquetados][y_tr[etiquetados] == 0, 1], color=AZUL, s=64,
               edgecolors=TEXTO, linewidths=1.1, zorder=5)
    ax.scatter(X_tr[etiquetados][y_tr[etiquetados] == 1, 0],
               X_tr[etiquetados][y_tr[etiquetados] == 1, 1], color=ROJO, s=64,
               edgecolors=TEXTO, linewidths=1.1, zorder=5)
    titulo(ax, corto, largo)
    # La exactitud va dentro del panel: en el subtítulo sería tan larga que empujaría los dos
    # paneles y dejaría un hueco enorme entre ellos.
    anotar(ax, ("exactitud en prueba: %.2f" % nota).replace(".", ","), xy=(0.0, 0.0),
           xytext=pos, color=TEXTO, flecha=False, align="left" if pos[0] < 0.5 else "right")
    ax.set_xlabel("primera variable")
    rejilla(ax, "both")
    numeros(ax)

ejes[0].set_ylabel("segunda variable")
anotar(ejes[0], "con 12 ejemplos, la recta\ncae donde no toca", xy=(0.0, 0.0),
       xytext=(0.03, 0.90), color=TEXTO, flecha=False)
anotar(ejes[1], "las 138 filas sin etiquetar\nhan movido la frontera", xy=(0.0, 0.0),
       xytext=(0.97, 0.88), color=TEXTO, flecha=False, align="right")

guardar(fig, "semi-supervisado-frontera-con-12-etiquetas")
