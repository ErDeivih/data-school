"""inicializacion-de-pesos-1.py — la escala de los pesos decide si la señal llega al final.

Izquierda: desviación típica de las activaciones capa a capa en una red ReLU de 10 capas y 256
unidades, con tres inicializaciones. Con desviación 0,01 la señal se divide por 10¹⁰; con He se
mantiene.
Derecha: el factor que multiplica la varianza en cada capa, 0,5·n_in·Var(w), frente al fan-in.
He vale 1 para cualquier tamaño de capa y un valor fijo no puede acertar en todos.
La figura de la página de inicialización de pesos (fase 7).
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

ANCHO = 256
CAPAS = 10

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: simulación de la señal a través de diez capas ------------------------
ax = ejes[0]
entrada = azar.normal(size=ANCHO)                  # activaciones de partida, desviación 1
inicializaciones = (("std 0,01", 0.01, ROJO),
                    ("Xavier", np.sqrt(2.0 / (ANCHO + ANCHO)), NARANJA),
                    ("He", np.sqrt(2.0 / ANCHO), VERDE))
for nombre, escala, color in inicializaciones:
    azar_capas = np.random.default_rng(7)          # la misma tirada para las tres: solo cambia la escala
    x = entrada.copy()
    stds = []
    for _ in range(CAPAS):
        w = azar_capas.normal(0.0, escala, size=(ANCHO, ANCHO))
        x = np.maximum(0.0, w @ x)                 # capa lineal seguida de ReLU
        stds.append(float(x.std()))
    ax.semilogy(np.arange(1, CAPAS + 1), stds, color=color, linewidth=1.8, marker="o",
                markersize=4)
# Sin leyenda: cada curva lleva su nota de color en el hueco que deja libre por debajo.
anotar(ax, "σ = 0,01: la señal se divide por 10¹⁰\nen diez capas y la red queda muerta",
       xy=(9.0, 1e-9), xytext=(0.30, 0.05), color=ROJO)
anotar(ax, "Xavier con ReLU: pierde la mitad\nde la varianza en cada capa",
       xy=(6.5, 0.06), xytext=(0.60, 0.42), color=NARANJA)
anotar(ax, "He: la desviación se queda cerca de 1\nen todas las capas",
       xy=(8.0, 0.63), xytext=(0.50, 0.96), color=VERDE)
titulo(ax, "Diez capas con ReLU: dónde se apaga la señal",
       "desviación típica de las activaciones, capa a capa, con una entrada de desviación 1")
ax.set_xlabel("capa")
ax.set_ylabel("desviación típica de las activaciones")
ax.set_xticks(np.arange(1, CAPAS + 1, 2))
ax.set_ylim(1e-10, 6.0)         # el hueco de arriba queda libre para la nota de He
rejilla(ax)
numeros(ax, ejes="x")

# --- Derecha: el factor por capa según el fan-in --------------------------------------
ax = ejes[1]
n_in = np.logspace(np.log10(64.0), np.log10(4096.0), 300)
# El 0,5 es lo que se lleva ReLU al apagar la mitad de las contribuciones
factor_std = 0.5 * n_in * 0.01 ** 2
factor_xavier = 0.5 * n_in * (2.0 / (n_in + n_in))
factor_he = 0.5 * n_in * (2.0 / n_in) * np.ones_like(n_in)
ax.plot(n_in, factor_std, color=ROJO, linewidth=1.8, label="σ fija de 0,01")
ax.plot(n_in, factor_xavier, color=NARANJA, linewidth=1.8, label="Xavier: 2 / (n_in + n_out)")
ax.plot(n_in, factor_he, color=VERDE, linewidth=1.8, label="He: 2 / n_in")
ax.axhline(1.0, color=TEXTO, linewidth=1.2, linestyle="--")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(1e-3, 6.0)          # por encima de 1 no hay ninguna curva: ahí cabe la nota
anotar(ax, "aquí la varianza se conserva:\nla señal ni crece ni se apaga",
       xy=(1000.0, 1.0), xytext=(0.30, 0.93), color=TEXTO)
anotar(ax, "un valor fijo solo acierta\nen una capa concreta",
       xy=(300.0, 0.015), xytext=(0.02, 0.075), color=ROJO)
titulo(ax, "La receta se elige para que este factor valga 1",
       "factor que multiplica la varianza en cada capa, según el fan-in")
ax.set_xlabel("fan-in de la capa (n_in)")
ax.set_ylabel("factor de la varianza por capa")
ax.legend(loc="lower right")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "inicializacion-senal-por-capa")
