"""gmm-1.py — la mezcla vista desde dentro: la densidad suma dos campanas y cada punto
reparte su pertenencia entre las dos. Pagina de mezclas gaussianas (fase 6)."""

import numpy as np

from comun import *

estilo()

# Los seis puntos del ejemplo de la pagina: dos bloques evidentes, -1, 0, 1 y 4, 5, 6.
datos = np.array([-1.0, 0.0, 1.0, 4.0, 5.0, 6.0])


def densidad(x, mu, var):
    """Densidad normal escrita a mano: no hace falta scipy para seis números."""
    return np.exp(-((x - mu) ** 2) / (2 * var)) / np.sqrt(2 * np.pi * var)


# --- EM a mano, que es lo que hace sklearn por dentro.
mu = np.array([0.0, 4.0])       # arranque: dos centros distintos, como en el ejemplo
var = np.array([1.0, 1.0])
pi = np.array([0.5, 0.5])       # pesos de cada componente
log_verosimilitud = []

for _ in range(6):
    # Paso E: la responsabilidad r_ik es la densidad de la componente k ponderada por su
    # peso, normalizada entre las dos para que sume 1 en cada observacion.
    r = np.array([pi[k] * densidad(datos, mu[k], var[k]) for k in range(2)])
    r = r / r.sum(axis=0)
    # Paso M: cada parametro se recalcula ponderando cada punto por su responsabilidad.
    # Los pesos suman 1, asi que la varianza se divide entre la suma de responsabilidades
    # (suma de pesos = 1) y no entre el numero de puntos.
    n_k = r.sum(axis=1)
    mu = (r * datos).sum(axis=1) / n_k
    var = (r * (datos - mu[:, None]) ** 2).sum(axis=1) / n_k
    pi = n_k / len(datos)
    log_verosimilitud.append(float(np.log(np.array(
        [pi[k] * densidad(datos, mu[k], var[k]) for k in range(2)]).sum(axis=0)).sum()))

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: las dos campanas y la suma de las dos.
malla = np.linspace(-3.5, 9.5, 400)
campana_1 = pi[0] * densidad(malla, mu[0], var[0])
campana_2 = pi[1] * densidad(malla, mu[1], var[1])

ejes[0].fill_between(malla, campana_2, campana_1 + campana_2, color=MORADO, alpha=0.25,
                     label="aporta la componente 2")
ejes[0].fill_between(malla, 0, campana_1, color=AZUL, alpha=0.25,
                     label="aporta la componente 1")
ejes[0].plot(malla, campana_1, color=AZUL, linewidth=1.6)
ejes[0].plot(malla, campana_2, color=MORADO, linewidth=1.6)
ejes[0].plot(malla, campana_1 + campana_2, color=TEXTO, linewidth=1.8, label="mezcla")
# Los datos van abajo, sobre el eje, para no tapar las curvas.
ejes[0].scatter(datos, np.zeros_like(datos), s=48, color=ROJO, marker="v", zorder=5,
                label="observaciones")
# El colchon de texto va apartado, en el valle que queda entre las dos campanas y a la
# derecha de la segunda: ahi no hay ni curvas ni puntos.
anotar(ejes[0], "mu_1 = {}\ny mu_2 = {}".format(coma(round(mu[0], 2)), coma(round(mu[1], 2))),
       xy=(float(mu[1]), 0.02), xytext=(0.72, 0.55), color=TEXTO, flecha=False)
titulo(ejes[0], "La densidad es la suma de dos campanas",
       "cada componente pesa la mitad; juntas forman la curva negra")
ejes[0].set_xlabel("valor de la variable")
ejes[0].set_ylabel("densidad")
ejes[0].legend(loc="upper left", fontsize=8)
rejilla(ejes[0], eje="y")
numeros(ejes[0], ejes="x")

# --- Derecha: la responsabilidad de cada punto, que es lo que K-means no sabe hacer.
# Tres puntos: uno pegado a un centro, otro pegado al otro y uno justo en medio.
consulta = np.array([0.5, 2.5, 5.5])
r_consulta = np.array([pi[k] * densidad(consulta, mu[k], var[k]) for k in range(2)])
r_consulta = r_consulta / r_consulta.sum(axis=0)

posiciones = np.arange(len(consulta))
ejes[1].barh(posiciones, r_consulta[0], color=AZUL, alpha=0.85, label="componente 1")
ejes[1].barh(posiciones, r_consulta[1], left=r_consulta[0], color=MORADO, alpha=0.85,
             label="componente 2")
for i, x in enumerate(consulta):
    ejes[1].text(1.02, i, f"{r_consulta[1, i]:.0%} y {r_consulta[0, i]:.0%}", va="center",
                 fontsize=8.5, color=TEXTO)
anotar(ejes[1], "x = 2,5 está justo en medio: 50 % y 50 %.\nEse punto es el que una etiqueta dura esconde",
       xy=(0.5, 1.0), xytext=(0.06, 0.86), color=TEXTO, flecha=False)
titulo(ejes[1], "Pertenencia blanda, no etiqueta dura",
       f"responsabilidad de cada punto; log-verosimilitud final {coma(round(log_verosimilitud[-1], 3))}")
ejes[1].set_yticks(posiciones)
ejes[1].set_yticklabels([f"x = {coma(v)}" for v in consulta])
ejes[1].set_xlabel("responsabilidad (suma 1 en cada barra)")
ejes[1].set_xlim(0, 1.35)
ejes[1].legend(loc="lower right", fontsize=8)
rejilla(ejes[1], eje="x")
numeros(ejes[1], ejes="x")

guardar(fig, "gmm-mezcla-y-pertenencia-blanda")
