"""dbscan-y-hdbscan-1.py — quien es central, quien es borde y quien es ruido, y como se
elige el radio eps. Pagina de DBSCAN y HDBSCAN (fase 6)."""

import numpy as np
from sklearn.neighbors import NearestNeighbors

from comun import *

estilo()
azar = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# Tres racimos con densidades distintas: el de arriba a la derecha es mas disperso, asi que
# con un eps fijo sus puntos se quedan fuera antes que los de los otros dos.
racimos = [azar.normal([0.0, 0.0], 0.42, (60, 2)),
           azar.normal([2.4, 0.5], 0.50, (55, 2)),
           azar.normal([1.3, 2.6], 1.05, (40, 2))]
# Puntos sueltos por todo el recuadro: son los candidatos a ruido.
sueltos = azar.uniform([-1.6, -1.6], [3.8, 4.2], (35, 2))
X = np.vstack(racimos + [sueltos])

EPS = 0.55          # radio de la vecindad
MIN_PTS = 5         # incluye el propio punto: son 4 vecinos mas

# Para cada punto se mira cuantos vecinos caen dentro del radio. Con NearestNeighbors el
# propio punto sale como vecino a distancia 0, por eso se cuentan MIN_PTS columnas enteras.
vecinos = NearestNeighbors(radius=EPS).fit(X)
cuantos = np.array([len(v) for v in vecinos.radius_neighbors(X, return_distance=False)])

es_central = cuantos >= MIN_PTS
# Un punto es de borde si no es central pero cae dentro del radio de uno central; si no es
# ni una cosa ni la otra, es ruido. Las tres categorias son excluyentes.
cerca_de = vecinos.radius_neighbors(X, return_distance=False)
es_borde = np.array([(not central) and any(es_central[j] for j in js)
                     for central, js in zip(es_central, cerca_de)])
es_ruido = ~es_central & ~es_borde

ejes[0].scatter(X[es_ruido, 0], X[es_ruido, 1], s=42, color=ROJO, marker="x",
                label="ruido: nadie denso lo alcanza")
ejes[0].scatter(X[es_borde, 0], X[es_borde, 1], s=30, color=NARANJA, marker="s",
                label="punto de borde")
ejes[0].scatter(X[es_central, 0], X[es_central, 1], s=30, facecolor="none", edgecolor=AZUL,
                linewidth=1.2, label=f"punto central: {MIN_PTS} o más vecinos")
# El circulo se dibuja sobre un punto central concreto: dentro tienen que caber MIN_PTS.
elegido = int(np.argmax(es_central))
circulo = plt.Circle(X[elegido], EPS, facecolor=CIAN, alpha=0.18, edgecolor=CIAN, zorder=1)
ejes[0].add_patch(circulo)
anotar(ejes[0], "aquí dentro caben 5 puntos:\nese punto es central",
       xy=(float(X[elegido, 0]), float(X[elegido, 1])), xytext=(0.44, 0.90), color=CIAN)
titulo(ejes[0], "Central, de borde y ruido",
       f"eps = {coma(EPS)} y minPts = {MIN_PTS}, contando el propio punto")
ejes[0].set_xlabel("variable 1")
ejes[0].set_ylabel("variable 2")
ejes[0].set_ylim(-2.1, 4.9)
ejes[0].legend(loc="lower right", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: la curva de la k-esima distancia, ordenada de menor a mayor. El codo es el
# candidato a eps: por debajo quedan las zonas densas y por encima los puntos aislados.
k = MIN_PTS - 1
distancias = np.sort(NearestNeighbors(n_neighbors=k + 1).fit(X)
                     .kneighbors(X, return_distance=True)[0][:, -1])

ejes[1].plot(np.arange(len(distancias)), distancias, color=MORADO, linewidth=1.8)
ejes[1].axhline(EPS, color=ROJO, linewidth=1.3, linestyle="--")
anotar(ejes[1], f"eps = {coma(EPS)}: deja fuera\nlos {int((distancias > EPS).sum())} puntos más aislados",
       xy=(float(np.argmax(distancias > EPS)), EPS), xytext=(0.06, 0.88), color=ROJO)
anotar(ejes[1], "el codo: aquí la curva deja de ser plana\ny empiezan los puntos sueltos",
       xy=(float(np.argmax(distancias > 1.0)), 1.05), xytext=(0.40, 0.42), color=MORADO)
titulo(ejes[1], "La curva para elegir eps",
       "distancia al cuarto vecino de cada punto, ordenada de menor a mayor")
ejes[1].set_xlabel("puntos, ordenados por aislamiento")
ejes[1].set_ylabel(f"distancia al vecino {k}")
rejilla(ejes[1], eje="y")
numeros(ejes[1], ejes="both")

guardar(fig, "dbscan-tipos-de-punto-y-eleccion-de-eps")
