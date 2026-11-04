"""estimacion-bayesiana-map-1.py — el prior, la verosimilitud y el posterior, y el reparto
entre ellos según cuántos datos haya. Figura de la página estimacion-bayesiana-map."""

import numpy as np
from scipy import stats

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(7.9, 3.9))

# --- Izquierda: prior, verosimilitud y posterior de la moneda ----------------------
eje = ejes[0]
caras, cruces = 7, 3
a_prior, b_prior = 3.0, 3.0
a_post, b_post = a_prior + caras, b_prior + cruces        # conjugada: Beta(10, 6)

p = np.linspace(0.001, 0.999, 1500)
prior = stats.beta.pdf(p, a_prior, b_prior)
posterior = stats.beta.pdf(p, a_post, b_post)
verosimilitud = p ** caras * (1 - p) ** cruces
verosimilitud = verosimilitud / verosimilitud.max() * posterior.max()   # reescalada

mle = caras / (caras + cruces)
mapa = (a_post - 1) / (a_post + b_post - 2)
limite_bajo, limite_alto = stats.beta.ppf(0.025, a_post, b_post), stats.beta.ppf(0.975, a_post, b_post)

eje.axvspan(limite_bajo, limite_alto, color=VERDE, alpha=0.10, zorder=0)
eje.plot(p, prior, color=MORADO, linewidth=1.5, linestyle="--", label="prior  Beta(3, 3)")
eje.plot(p, verosimilitud, color=REJILLA, linewidth=1.4, linestyle=":",
         label="verosimilitud (reescalada)")
eje.plot(p, posterior, color=AZUL, linewidth=1.9, label="posterior  Beta(10, 6)")
eje.set_xlim(0, 1)
eje.set_ylim(0, posterior.max() * 1.5)
alto = eje.get_ylim()[1]
for valor, color, etiqueta in ((mapa, VERDE, "MAP 0,643"), (mle, ROJO, "MLE 0,700")):
    eje.axvline(valor, color=color, linewidth=1.3)
    eje.text(valor + 0.012, alto * 0.99, etiqueta, color=color, fontsize=8, rotation=90, va="top")
eje.text((limite_bajo + limite_alto) / 2, alto * 0.05,
         "95 % creíble", color=VERDE, fontsize=8, ha="center")
titulo(eje, "El MAP es el pico del posterior, no el del MLE",
       "7 caras y 3 cruces, con prior Beta(3, 3)")
eje.set_xlabel("p, probabilidad de cara")
eje.set_ylabel("densidad")
eje.legend(loc="upper left", fontsize=8)
rejilla(eje)
numeros(eje)

# --- Derecha: quién manda, el prior o los datos, según el tamaño de la muestra -----
eje = ejes[1]
ns = np.arange(2, 261)
proporcion = 0.7
mapa_n = (a_prior + proporcion * ns - 1) / (a_prior + b_prior + ns - 2)
eje.plot(ns, proporcion * np.ones_like(ns), color=ROJO, linewidth=1.8, label="MLE = k/n = 0,700")
eje.plot(ns, mapa_n, color=AZUL, linewidth=1.8, label="MAP con prior Beta(3, 3)")
eje.axhline((a_prior - 1) / (a_prior + b_prior - 2), color=MORADO, linewidth=1.3, linestyle="--")
eje.text(250, 0.508, "lo que cree el prior: 0,5", color=MORADO, fontsize=8, ha="right")
eje.set_xlim(0, 260)
eje.set_ylim(0.45, 0.76)
anotar(eje, "con pocos datos manda el prior;\ncon muchos, los datos",
       xy=(5, mapa_n[3]), xytext=(0.28, 0.40))
titulo(eje, "El prior no se olvida: los datos lo superan",
       "la misma proporción observada, 0,7")
eje.set_xlabel("n, número de lanzamientos")
eje.set_ylabel("estimación de p")
eje.legend(loc="upper left", fontsize=8)
rejilla(eje)
numeros(eje)

guardar(fig, "bayes-prior-posterior-y-map")
