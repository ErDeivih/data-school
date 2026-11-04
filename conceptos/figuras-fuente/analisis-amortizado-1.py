"""analisis-amortizado-1.py — el total de copias y los picos que se ven en cada inserción.

Izquierda: copias acumuladas al insertar n elementos, en escala logarítmica, según dos políticas de
crecimiento. Duplicar la capacidad suma n − 1 copias; crecer de uno en uno suma n(n−1)/2, que es la
diferencia entre O(n) y Θ(n²) al insertar n elementos.
Derecha: el coste real de cada una de las primeras 40 inserciones (copias más la propia inserción).
Los picos son de verdad y ocurren en las potencias de dos, pero cada vez están más separados: la
media no crece y se queda por debajo de 3, que es la cota amortizada.
La figura de la página de análisis amortizado (fase 10).
"""

import numpy as np

from comun import *

estilo()


def copias_acumuladas(n_max, politica):
    """Copias que se llevan a cabo al insertar 1, 2, ..., n_max elementos."""
    capacidad, tam, copias = 1, 0, 0
    serie = np.zeros(n_max + 1)
    for i in range(1, n_max + 1):
        if tam == capacidad:                    # no cabe: hay que ampliar
            copias += tam                       # se traslada todo lo guardado
            capacidad = capacidad * 2 if politica == "doble" else capacidad + 1
        tam += 1
        serie[i] = copias
    return serie


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: el total de copias de las dos políticas --------------------------------
ax = ejes[0]
# Una potencia de dos: ahí la suma de copias es exactamente n − 1 y la cuenta sale redonda.
N_MAX = 2 ** 18
doble = copias_acumuladas(N_MAX, "doble")
uno = copias_acumuladas(N_MAX, "uno")
# Se dibujan solo unos cuantos n, repartidos en escala logarítmica: la curva es monótona.
puntos = np.unique(np.logspace(0, np.log10(N_MAX), 70).astype(int))
n = puntos[1:]

ax.loglog(n, doble[n], color=AZUL, linewidth=2.2, zorder=4, label="duplicar la capacidad")
ax.loglog(n, uno[n], color=ROJO, linewidth=2.2, zorder=3, label="crecer de uno en uno")
veces = float(uno[N_MAX] / doble[N_MAX])
anotar(ax, f"duplicar: {int(doble[N_MAX]):,} copias en total".replace(",", ".")
       + "\n(justo n − 1, una por inserción)",
       xy=(N_MAX, float(doble[N_MAX])), xytext=(0.03, 0.94), color=AZUL, flecha=False)
anotar(ax, f"crecer de uno en uno:\n{int(uno[N_MAX]):,} copias".replace(",", ".")
       + f", {veces:,.0f} veces más".replace(",", "."),
       xy=(N_MAX, float(uno[N_MAX])), xytext=(0.03, 0.80), color=ROJO, flecha=False)
titulo(ax, "Duplicar o sumar un hueco: la diferencia es el cuadrado",
       "copias acumuladas al insertar n elementos, en escala logarítmica")
ax.set_xlabel("inserciones (n)")
ax.set_ylabel("copias acumuladas")
ax.set_ylim(0.5, 5e13)          # el hueco de arriba queda libre para las dos notas
ax.legend(loc="lower right", fontsize=8.5)
rejilla(ax, eje="both")

# --- Derecha: el coste real de cada inserción ------------------------------------------
ax = ejes[1]
n_pequeno = np.arange(1, 41)
copias = np.diff(copias_acumuladas(40, "doble"))
coste = copias + 1.0                      # copiar lo que había y colocar el nuevo
picos = copias > 0                        # en estas inserciones hubo que ampliar

ax.bar(n_pequeno[~picos], coste[~picos], width=0.72, color=AZUL, alpha=0.85, zorder=3,
       label="inserción normal")
ax.bar(n_pequeno[picos], coste[picos], width=0.72, color=ROJO, alpha=0.9, zorder=4,
       label="ampliación: copia todo")
media = float(coste.sum() / n_pequeno.size)
ax.axhline(media, color=TEXTO, linewidth=1.3, linestyle="--", zorder=5,
           label=f"media real ({media:.2f})".replace(".", ","))
ax.axhline(3.0, color=VERDE, linewidth=1.3, linestyle=":", zorder=5,
           label="cota amortizada: 3")
anotar(ax, "la ampliación de la inserción 33 copia 32;\ndespués vienen 32 inserciones baratas",
       xy=(33.0, 33.0), xytext=(0.20, 0.70), color=ROJO)
titulo(ax, "Cada ampliación cuesta O(n), pero cada vez toca menos",
       "coste de las primeras 40 inserciones; los picos caen en 1, 2, 4, 8, 16 y 32")
ax.set_xlabel("inserción")
ax.set_ylabel("copias más la inserción")
ax.set_xlim(0, 41)
ax.set_ylim(0, 40)
ax.set_yticks([0, 3, 10, 20, 33])
ax.legend(loc="upper left", fontsize=8, ncol=2, columnspacing=1.0)
rejilla(ax)

guardar(fig, "amortizado-copias-y-picos")
