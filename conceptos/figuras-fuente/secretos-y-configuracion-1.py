"""secretos-y-configuracion-1.py — por qué alargar un secreto vale más que complicarlo: cada
caracter multiplica el espacio de busqueda. La figura de la pagina (fase 11)."""

import numpy as np

from comun import *

estilo()

MINUSCULAS, ALFANUMERICO, INTENTOS = 26, 62, 1e9      # simbolos por caracter y intentos por segundo
longitudes = np.arange(6, 17)
# En el dominio logaritmico: 62^24 desborda el float de 64 bits y saldria una curva falsa.
log_segundos_min = longitudes * np.log2(MINUSCULAS) - np.log2(2 * INTENTOS)
log_segundos_alf = longitudes * np.log2(ALFANUMERICO) - np.log2(2 * INTENTOS)
UN_ANO, MIL_ANOS = 3600 * 24 * 365, 3600 * 24 * 365 * 1000

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.3))

# --- Izquierda: el tiempo de agotamiento, en escala logaritmica ---------------
ejes[0].plot(longitudes, log_segundos_min, color=ROJO, linewidth=2.0,
             label="minusculas (26 simbolos)")
ejes[0].plot(longitudes, log_segundos_alf, color=VERDE, linewidth=2.0,
             label="alfanumerico (62 simbolos)")
ejes[0].axhline(np.log2(MIL_ANOS), color=MORADO, linestyle="--", linewidth=1.2)
ejes[0].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)      # un segundo

anotar(ejes[0], "mil anos: por encima de aqui el ataque directo no llega",
       xy=(15.6, np.log2(MIL_ANOS)), xytext=(0.20, 0.72), color=MORADO)
anotar(ejes[0], "8 minusculas: 209 s y ya no hay nada que hacer",
       xy=(8, log_segundos_min[2]), xytext=(0.05, 0.24), color=ROJO)
anotar(ejes[0], "16 caracteres: millones de anos",
       xy=(16, log_segundos_min[10]), xytext=(0.38, 0.12), color=VERDE)

ejes[0].set_xlabel("caracteres del secreto")
ejes[0].set_ylabel("log2 de los segundos para agotarlo")
ejes[0].set_xlim(6, 16)
ejes[0].set_ylim(-2, 42)
ejes[0].legend(loc="upper left")
titulo(ejes[0], "Cada caracter multiplica el trabajo",
       "el eje va en log2: cada 10 unidades son mil veces más tiempo")
rejilla(ejes[0])
numeros(ejes[0], "x")

# --- Derecha: cuanto anade cada caracter, en bits -----------------------------
ancho = 0.38
posiciones = np.arange(2)
valores = [np.log2(MINUSCULAS), np.log2(ALFANUMERICO)]
ejes[1].bar(posiciones - ancho / 2, valores, width=ancho, color=[ROJO, VERDE])
for i, (bits, color) in enumerate(zip(valores, [ROJO, VERDE])):
    ejes[1].text(i - ancho / 2, bits + 0.12, f"{bits:.2f} bits", ha="center", fontsize=9,
                 color=color)

anotar(ejes[1], "pasar de 26 a 62 simbolos anade 1,25 bits",
       xy=(1 - ancho / 2, np.log2(ALFANUMERICO)), xytext=(0.02, 0.95), color=VERDE)
anotar(ejes[1], "cuatro caracteres de más anaden 18,8 bits",
       xy=(0, np.log2(MINUSCULAS)), xytext=(0.68, 0.30), color=ROJO)

ejes[1].set_xticks(posiciones)
ejes[1].set_xticklabels(["minusculas\n(26 simbolos)", "alfanumerico\n(62 simbolos)"], fontsize=9)
ejes[1].set_xlim(-0.6, 2.0)
ejes[1].set_ylim(0, 8.6)
ejes[1].set_ylabel("bits que anade cada caracter")
titulo(ejes[1], "Complicar el alfabeto rinde poco",
       "alargar cuatro caracteres anade más fuerza que cambiar de alfabeto entero")
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "secretos-longitud-y-alfabeto")
