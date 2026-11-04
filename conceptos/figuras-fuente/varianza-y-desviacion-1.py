"""varianza-y-desviacion-1.py — la media no basta, y las desviaciones no se suman.

Arriba: dos empresas con la MISMA media de 30 minutos y dispersiones incomparables.
Abajo a la izquierda: cambiar la escala (x3) multiplica la desviación por 3 y la varianza por 9.
Abajo a la derecha: la desviación de la suma de dos dados es menor que la suma de las
desviaciones, porque lo que se suma son las varianzas.
"""

import numpy as np

from comun import *

estilo()

# --- Panel superior: misma media, distinta dispersion -----------------------------
azar = np.random.default_rng(7)
n = 4000
# Empresa A: muy regular. Empresa B: misma media, pero la mitad de las veces 10 y la mitad 50.
regular = 30 + azar.normal(0, 1.7, n)
irregular = np.where(azar.random(n) < 0.5, 10 + azar.normal(0, 3, n), 50 + azar.normal(0, 3, n))

# Arriba un panel ancho (ocupa las dos columnas: la comparacion de las dos empresas se lee
# mejor asi y no deja un cuarto hueco vacio); abajo, los dos paneles de detalle.
fig = plt.figure(figsize=(10.8, 6.6))
huecos = fig.add_gridspec(2, 2)
sup = fig.add_subplot(huecos[0, :])
sup.hist(regular, bins=60, range=(0, 60), density=True, color=AZUL, alpha=0.65, label="empresa A")
sup.hist(irregular, bins=60, range=(0, 60), density=True, color=NARANJA, alpha=0.55, label="empresa B")
sup.axvline(30, color=ROJO, linewidth=1.6, linestyle="--")
# Las notas van en coordenadas del eje (0-1): la franja de arriba queda libre por encima de
# las dos distribuciones, y las otras dos, en los huecos a los lados de la campana azul.
sup.set_ylim(0, 0.32)
anotar(sup, "media de las dos = 30 min", xy=(30, 0.255), xytext=(0.51, 0.90), color=ROJO)
anotar(sup, "A casi siempre cumple", xy=(31, 0.235), xytext=(0.63, 0.60), color=AZUL)
anotar(sup, "B no dice nada de un reparto suelto", xy=(10, 0.055), xytext=(0.03, 0.55),
       color=NARANJA)
sup.set_xlabel("minutos por reparto")
sup.set_ylabel("densidad")
titulo(sup, "Misma media, dos empresas opuestas",
       "las dos reparten 30 minutos de media y no se parecen en nada")
sup.legend(loc="upper right")
numeros(sup)
rejilla(sup)

# --- El cambio de escala ----------------------------------------------------------
esc = fig.add_subplot(huecos[1, 0])
dado = np.arange(1, 7, dtype=float)
var_dado = float(dado.var())                      # 2,9167
barras = esc.bar(
    ["desviación\noriginal", "desviación\nx3", "varianza\noriginal", "varianza\nx3"],
    [np.sqrt(var_dado), 3 * np.sqrt(var_dado), var_dado, 9 * var_dado],
    width=0.6, color=[AZUL, AZUL, MORADO, MORADO],
)
for b, v in zip(barras, [np.sqrt(var_dado), 3 * np.sqrt(var_dado), var_dado, 9 * var_dado]):
    esc.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v:.2f}".replace(".", ","),
             ha="center", color=TEXTO, fontsize=9)
esc.set_ylim(0, 31)
# La nota larga va a la izquierda (encima de las barras bajas) con el texto pegado a su
# derecha, para que la flecha salga hacia la barra morada y no lo cruce.
anotar(esc, "x3", xy=(0.80, 5.2), xytext=(0.30, 0.30), color=AZUL, align="right")
anotar(esc, "x9, porque la varianza va en unidades al cuadrado", xy=(2.72, 26.3),
       xytext=(0.68, 0.60), color=MORADO, align="right")
esc.set_ylabel("valor")
titulo(esc, "Escala x3: distinto efecto en sigma y varianza",
       "la varianza va en unidades al cuadrado")
numeros(esc, ejes="y")
rejilla(esc)

# --- Sumar desviaciones frente a sumar varianzas ---------------------------------
suma = fig.add_subplot(huecos[1, 1])
sd_dado = float(dado.std())
combinaciones = np.array([a + b for a in range(1, 7) for b in range(1, 7)], dtype=float)
sd_suma = float(combinaciones.std())
suma_ingenua = sd_dado + sd_dado
barras = suma.bar(
    ["sumar las\ndesviaciones", "raiz de sumar\nlas varianzas"],
    [suma_ingenua, sd_suma], width=0.5, color=[ROJO, VERDE],
)
for b, v in zip(barras, [suma_ingenua, sd_suma]):
    suma.text(b.get_x() + b.get_width() / 2, v + 0.06, f"{v:.4f}".replace(".", ","),
              ha="center", color=TEXTO, fontsize=10)
# La nota va en la esquina de arriba a la derecha, por encima de las dos barras, y la
# flecha baja hacia la barra roja sin pasar por encima del texto.
suma.set_ylim(0, 4.1)
anotar(suma, "infla el riesgo un 41 %", xy=(0.3, 3.4), xytext=(0.70, 0.93), color=ROJO)
suma.set_ylabel("desviación típica de la suma")
titulo(suma, "Sumar desviaciones infla el riesgo", "lo que se suma son las varianzas")
numeros(suma, ejes="y")
rejilla(suma)

guardar(fig, "varianza-dispersion-y-suma")
