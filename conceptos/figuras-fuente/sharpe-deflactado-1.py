"""sharpe-deflactado-1.py — el liston del ruido sube con el número de intentos y se come el
Sharpe que parecia bueno. La figura de la pagina de Sharpe deflactado (fase 9)."""

import numpy as np
from statistics import NormalDist

from comun import *

estilo()
Z = NormalDist()
GAMMA = 0.5772156649

T = 1200
SR = 0.15          # Sharpe por periodo del mejor backtest
SIGMA_SR = 0.05    # desviacion tipica de los Sharpes entre intentos
SESGO, CURTOSIS = -0.5, 6.0


def sr0_de(intentos):
    """Sharpe que se espera del mejor de N intentos cuando no hay ninguna habilidad."""
    if intentos <= 1:
        return 0.0
    return SIGMA_SR * ((1 - GAMMA) * Z.inv_cdf(1 - 1 / intentos)
                       + GAMMA * Z.inv_cdf(1 - 1 / (intentos * np.e)))


def dsr_de(intentos):
    den = np.sqrt(1 - SESGO * SR + (CURTOSIS - 1) / 4 * SR ** 2)
    return Z.cdf((SR - sr0_de(intentos)) * np.sqrt(T - 1) / den)


intentos = np.unique(np.round(np.logspace(0, 4, 400)).astype(int))
liston = np.array([sr0_de(n) for n in intentos])
dsr = np.array([dsr_de(n) for n in intentos])
cruces = np.where(liston > SR)[0]
cruce = int(intentos[cruces[0]]) if cruces.size else None

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.8), sharex=True)

# --- Arriba: el liston sube con los intentos y se cruza con el Sharpe observado ---
ejes[0].plot(intentos, liston, color=ROJO, linewidth=1.8)
ejes[0].axhline(SR, color=AZUL, linewidth=1.4, linestyle="--")
if cruce:
    ejes[0].axvline(cruce, color=MORADO, linewidth=1.0, linestyle=":")
    ejes[0].plot([cruce], [SR], "o", color=MORADO, markersize=4)
    # La nota del cruce baja al cuarto de panel que queda libre por debajo de la curva: en
    # (0,50, 0,20) la rejilla del 0,05 le cruzaba la primera línea (medido: 84 px).
    anotar(ejes[0], "con %d intentos el listón\nya ha superado tu Sharpe" % cruce,
           xy=(cruce, SR), xytext=(0.72, 0.40), color=MORADO)
titulo(ejes[0], "El listón: con más intentos sube el ruido",
       "el mejor Sharpe que da el azar cuando no hay ninguna habilidad")
ejes[0].set_ylabel("Sharpe por periodo")
# Los dos rótulos de las líneas van a franjas libres de rejilla: arriba a la izquierda (por
# debajo pasa la curva roja) y a la derecha por debajo de la raya azul. Donde estaban, junto a
# su línea, la curva roja les pasaba por encima (129 px dentro de «tu Sharpe observado…»).
anotar(ejes[0], "el mejor resultado que da el azar", xy=(intentos[-1], liston[-1]),
       xytext=(0.03, 0.87), color=ROJO, flecha=False)
anotar(ejes[0], "tu Sharpe observado, 0,15", xy=(intentos[-1], SR),
       xytext=(0.985, 0.63), color=AZUL, flecha=False, align="right")
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- Abajo: lo mismo visto como probabilidad de que el Sharpe sea real ---
ejes[1].plot(intentos, dsr, color=VERDE, linewidth=1.8)
ejes[1].axhline(0.95, color=REJILLA, linewidth=1.0, linestyle="--")
anotar(ejes[1], "0,95: se puede defender ante un escéptico", xy=(intentos[-1], 0.95),
       xytext=(0.985, 0.83), color=REJILLA, flecha=False, align="right")
ejes[1].axhline(0.5, color=TEXTO, linewidth=0.8, alpha=0.4)
# La nota del 0,5 baja al hueco de abajo a la izquierda: pegada a su raya, la curva verde la
# partía en dos (medido: 116 px de curva dentro del texto).
anotar(ejes[1], "0,5: a partir de aquí\nlo explica el ruido", xy=(intentos[0], 0.5),
       xytext=(0.03, 0.12), color=TEXTO, flecha=False)
if cruce:
    ejes[1].plot([cruce], [dsr_de(cruce)], "o", color=MORADO, markersize=4)
    # La nota del mismo backtest va al hueco entre las rejillas de 0,6 y 0,8, a la derecha de
    # la curva, y desde ahí baja al punto morado.
    anotar(ejes[1], "mismo backtest, mismo 0,15:\nsolo cambia cuántas veces lo buscaste",
           xy=(cruce, dsr_de(cruce)), xytext=(0.60, 0.665), color=MORADO)
titulo(ejes[1], "El veredicto: ¿es habilidad o suerte?",
       "probabilidad de que el Sharpe observado sea de verdad")
ejes[1].set_xlabel("configuraciones probadas (escala logarítmica)")
ejes[1].set_ylabel("Sharpe deflactado")
ejes[1].set_ylim(-0.02, 1.06)
rejilla(ejes[1])
numeros(ejes[1], "y")
# El eje x va en escala logarítmica porque los intentos son potencias de diez (1, 10, 100,
# 1.000, 10.000). En escala lineal los tres primeros ticks caían a menos de 6 px uno de otro:
# las etiquetas «1», «10» y «100» se solapaban entre sí (medido: tres solapes, de 9 px y de
# 13,8 px) y la curva entera quedaba pegada al borde izquierdo, con medio panel vacío a la
# derecha. Con log los cinco ticks se reparten a lo ancho.
ejes[0].set_xscale("log")
ejes[1].set_xscale("log")
ejes[0].minorticks_off()
ejes[1].minorticks_off()
# Las etiquetas se ponen DESPUES de numeros() y de la escala: si se ponen antes, el formateador
# de la coma decimal las vuelve a pasar y "10" acaba escrito "10,0".
ejes[1].set_xticks([1, 10, 100, 1000, 10000])
ejes[1].set_xticklabels(["1", "10", "100", "1.000", "10.000"])

guardar(fig, "sharpe-deflactado-el-liston-del-ruido")
