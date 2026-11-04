"""estimadores-y-propiedades-1.py — insesgadez no es eficiencia: la media y la mediana
frente a una población normal y frente a una de cola larga. Figura de la página
estimadores-y-propiedades."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

n, replicas = 25, 4000
# La misma población del ejemplo: normal con σ² = 4 y Cauchy (centro 0, cola larguísima).
normal = azar.normal(0.0, 2.0, size=(replicas, n))
cauchy = azar.standard_cauchy(size=(replicas, n))

medias_normal = normal.mean(axis=1)
medianas_normal = np.median(normal, axis=1)
medias_cauchy = cauchy.mean(axis=1)
medianas_cauchy = np.median(cauchy, axis=1)

fig, ejes = plt.subplots(1, 2, figsize=(7.9, 3.9))

# --- Izquierda: con datos normales, la media es la más eficiente -------------------
eje = ejes[0]
eje.hist(medias_normal, bins=60, density=True, color=AZUL, alpha=0.55,
         label="media: varianza %.2f" % medias_normal.var())
eje.hist(medianas_normal, bins=60, density=True, color=NARANJA, alpha=0.55,
         label="mediana: varianza %.2f" % medianas_normal.var())
eje.axvline(0, color=ROJO, linewidth=1.2, linestyle="--")
eje.text(0.03, 0.94, "las dos están centradas en 0:\nlas dos son insesgadas",
         transform=eje.transAxes, fontsize=8, va="top")
titulo(eje, "Con datos normales, la media es más eficiente",
       "4.000 muestras de n = 25, normal con σ² = 4")
eje.set_xlabel("valor del estimador")
eje.set_ylabel("densidad")
eje.legend(loc="center right", fontsize=8)
rejilla(eje)
numeros(eje)

# --- Derecha: con cola larga, la mediana destroza a la media ----------------------
eje = ejes[1]
fuera = np.mean(np.abs(medias_cauchy) > 4)
eje.hist(medianas_cauchy, bins=60, range=(-4, 4), density=True, color=NARANJA, alpha=0.65,
         label="mediana: varianza %.2f" % medianas_cauchy.var())
eje.hist(medias_cauchy, bins=60, range=(-4, 4), density=True, color=AZUL, alpha=0.45,
         label="media: el %.0f %% ni cabe aquí" % (100 * fuera))
eje.axvline(0, color=ROJO, linewidth=1.2, linestyle="--")
eje.text(0.03, 0.96, "la media se escapa del dibujo:\nsu varianza no se estabiliza",
         transform=eje.transAxes, fontsize=8, va="top")
titulo(eje, "Con colas largas, la mediana destroza a la media",
       "las mismas muestras, ahora de una Cauchy")
eje.set_xlabel("valor del estimador")
eje.set_ylabel("densidad")
eje.legend(loc="center right", fontsize=8)
rejilla(eje)
numeros(eje)

guardar(fig, "estimadores-media-y-mediana")
