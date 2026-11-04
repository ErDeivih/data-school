"""tamano-de-posicion-1.py — con riesgo fijo el riesgo es el mismo en todas las operaciones y
la exposición no; y con correlación alta la diversificación tiene un suelo. Figura de la página
de Tamaño de posición (fase 9)."""

import numpy as np

from comun import *


def num(x, decimales=2):
    """Número con coma decimal, como se escribe en el portal."""
    return f"{x:.{decimales}f}".replace(".", ",")


estilo()

# --- Izquierda: riesgo fijo del 1 % sobre 50.000 EUR con entrada a 100 EUR. Lo que cambia entre
# las tres columnas es la distancia al stop, no lo que arriesgas.
capital, riesgo, entrada = 50_000.0, 0.01, 100.0
stops = np.array([98.0, 96.0, 90.0])
titulos = [f"stop en {s:.0f} €\n({num(100 * (s / entrada - 1), 0).replace('-', '−')} %)"
           for s in stops]
unidades = capital * riesgo / (entrada - stops)
nocional = 100 * unidades * entrada / capital

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

posiciones = np.arange(stops.size)
ejes[0].bar(posiciones, nocional, width=0.5, color=AZUL, alpha=0.85, zorder=2)
for xi, q, n in zip(posiciones, unidades, nocional):
    ejes[0].text(xi, n + 1.6, f"{q:.0f} títulos", ha="center", fontsize=9, color=TEXTO, zorder=3)
    ejes[0].text(xi, n / 2, f"{num(n, 0)} %", ha="center", va="center", fontsize=11,
                 color="white", zorder=3)
# La línea roja es lo único que no cambia con el stop: los euros que pierdes si salta.
ejes[0].axhline(100 * riesgo, color=ROJO, linewidth=1.6, linestyle="--", zorder=4)
ejes[0].set_xticks(posiciones)
ejes[0].set_xticklabels(titulos)
ejes[0].set_xlim(-0.65, 2.65)
ejes[0].set_ylim(0, 68)
anotar(ejes[0], f"la línea roja es lo que arriesgas: {num(capital * riesgo, 0)} €, el 1 %",
       xy=(2.45, 1.0), xytext=(0.98, 0.70), color=ROJO, align="right")
anotar(ejes[0], "el primer caso compra cinco veces más\nque el tercero sin arriesgar un euro más",
       xy=(0.0, nocional[0]), xytext=(0.03, 0.95), color=VERDE, flecha=False)
titulo(ejes[0], "Mismo riesgo, exposición distinta",
       "50.000 € de capital y un 1 % de riesgo por idea, con la entrada a 100 €")
ejes[0].set_xlabel("dónde pones el stop")
ejes[0].set_ylabel("nocional comprado (% del capital)")
rejilla(ejes[0])
numeros(ejes[0], ejes="y")

# --- Derecha: volatilidad de una cartera de N posiciones iguales, todas con la misma volatilidad
# y la misma correlación media. Al crecer N el primer término desaparece y queda sigma·raíz(rho).
largo = 200
n_posiciones = np.arange(1, largo + 1)
sigma = 0.25
for rho, color in zip((0.0, 0.3, 0.7), [VERDE, NARANJA, ROJO]):
    sigma_p = 100 * sigma * np.sqrt(1 / n_posiciones + rho * (n_posiciones - 1) / n_posiciones)
    ejes[1].plot(n_posiciones, sigma_p, color=color, linewidth=2.0,
                 label=f"correlación media {num(rho, 1)}")
    ejes[1].axhline(100 * sigma * np.sqrt(rho), color=color, linewidth=0.9, linestyle=":")
ejes[1].plot([5, 20], 100 * sigma * np.sqrt(1 / np.array([5, 20]) + 0.3 * (np.array([5, 20]) - 1) / np.array([5, 20])),
             linestyle="none", marker="o", markersize=6, color=NARANJA, zorder=5)
anotar(ejes[1], f"con correlación 0,7 el suelo es {num(100 * sigma * np.sqrt(0.7), 1)} %:\n"
                f"pasar de 5 a 20 posiciones no baja de ahí",
       xy=(20, 100 * sigma * np.sqrt(1 / 20 + 0.7 * 19 / 20)), xytext=(0.98, 0.93), color=ROJO,
       align="right")
anotar(ejes[1], f"con correlación 0 la misma cartera\nbaja del 25 % al {num(100 * sigma * np.sqrt(1 / 20), 2)} %",
       xy=(20, 100 * sigma * np.sqrt(1 / 20)), xytext=(0.98, 0.11), color=VERDE, align="right")
titulo(ejes[1], "La diversificación tiene un suelo",
       "volatilidad de una cartera de N posiciones iguales, cada una con un 25 % anual")
ejes[1].set_xlabel("número de posiciones")
ejes[1].set_ylabel("volatilidad de la cartera (%)")
ejes[1].set_xlim(1, 20)
ejes[1].set_ylim(0, 27)
ejes[1].legend(loc="lower left", fontsize=8)
rejilla(ejes[1])
numeros(ejes[1], ejes="both")

guardar(fig, "posicion-riesgo-fijo-y-correlación")
