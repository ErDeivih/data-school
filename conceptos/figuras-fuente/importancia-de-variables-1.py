"""importancia-de-variables-1.py — la importancia por impureza nunca llega a cero (ni con
ruido puro) mientras que la permutación sí lo distingue; y el sesgo de cardinalidad, que
reparte el peso según cuántos valores distintos tiene la columna. Figura de la página de
importancia de variables (fase 6)."""

import numpy as np

from comun import *

estilo()

# Las ocho variables del ejemplo de la página: las tres primeras informan de la etiqueta y
# las cinco últimas son ruido puro. Son los números que imprime el bloque de código, no
# otros inventados: así la figura y la tabla de la página cuentan lo mismo.
mdi = np.array([0.148, 0.370, 0.117, 0.073, 0.069, 0.070, 0.072, 0.081])
perm = np.array([0.163, 0.331, 0.106, -0.001, -0.007, 0.004, 0.005, -0.001])
nombres = ["x1", "x2", "x3", "ruido 4", "ruido 5", "ruido 6", "ruido 7", "ruido 8"]

# Las tres columnas aleatorias del segundo ejemplo: binaria, continua e identificador.
# Ninguna informa, y la impureza se va entera a las dos con más valores distintos.
card = ["binaria\n(2 valores)", "continua\n(cientos)", "identificador\n(400 valores)"]
mdi_card = np.array([0.008, 0.523, 0.469])
perm_card = np.array([0.0150, -0.0023, -0.0097])

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.4))

# --- Izquierda: las dos medidas sobre las mismas ocho variables, en barras horizontales.
filas = np.arange(len(nombres))
# Fondo gris detrás de las cinco de ruido: se ve de un golpe dónde acaba la señal. Va con
# zorder bajo para no tapar las barras.
ejes[0].axhspan(2.5, 7.5, color=REJILLA, alpha=0.16, zorder=0)
# Las dos barras de cada variable van desplazadas media altura arriba y abajo, para que la
# pareja se lea como un grupo y no como dos series mezcladas.
ejes[0].barh(filas - 0.19, mdi, height=0.36, color=AZUL, label="impureza (MDI)", zorder=3)
ejes[0].barh(filas + 0.19, perm, height=0.36, color=ROJO, label="permutación", zorder=3)
ejes[0].axvline(0, color=TEXTO, linewidth=0.9, zorder=4)
ejes[0].invert_yaxis()                     # x1 arriba: el ojo lee señal y luego ruido
ejes[0].set_yticks(filas, nombres)
ejes[0].set_xlim(-0.03, 0.50)
anotar(ejes[0], "el ruido también se lleva su parte:\nla impureza no baja de 0,07",
       xy=(0.081, 6), xytext=(0.36, 0.37), color=AZUL)
anotar(ejes[0], "la permutación lo manda a cero", xy=(0.004, 6), xytext=(0.36, 0.14),
       color=ROJO)
ejes[0].legend(loc="center right", bbox_to_anchor=(1.0, 0.62))
titulo(ejes[0], "Ocho variables, cinco de ruido: dos respuestas",
       "las tres primeras informan; las cinco de abajo no informan de nada")
ejes[0].set_xlabel("importancia (la impureza se normaliza y suma 1)")
rejilla(ejes[0], "x")
numeros(ejes[0], ejes="x")

# --- Derecha: el sesgo de cardinalidad con tres columnas que no informan de nada.
x = np.arange(3)
ejes[1].axhline(0, color=TEXTO, linewidth=0.9)
ejes[1].bar(x - 0.19, mdi_card, width=0.36, color=AZUL, label="impureza (MDI)", zorder=3)
ejes[1].bar(x + 0.19, perm_card, width=0.36, color=ROJO, label="permutación", zorder=3)
for xi, v in zip(x - 0.19, mdi_card):
    ejes[1].text(xi, v + 0.022, ("%.3f" % v).replace(".", ","), ha="center", fontsize=9,
                 color=AZUL)
anotar(ejes[1], "permutación:\n0,015 · −0,002 · −0,010", xy=(0.19, 0.015),
       xytext=(0.03, 0.66), color=ROJO)
ejes[1].set_xticks(x, card)
ejes[1].set_ylim(-0.09, 0.63)
ejes[1].set_xlim(-0.55, 2.55)
titulo(ejes[1], "Tres columnas de ruido: gana la de más valores",
       "ninguna informa de la etiqueta, que también es azar")
ejes[1].set_ylabel("importancia atribuida")
ejes[1].set_xlabel("naturaleza de la columna (todas aleatorias)")
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "importancia-de-variables-mdi-vs-permutación")
