"""bootstrap-1.py — de una sola muestra a la distribución de un estadístico. Con los ocho
tiempos de espera (y el valor extremo de 96 s): la mediana también tiene incertidumbre y el
bootstrap la fabrica remuestreando. Figura de la página de bootstrap."""

import numpy as np

from comun import *

estilo()

datos = np.array([12.0, 14.5, 13.2, 15.1, 12.8, 14.0, 13.7, 96.0])
azar = np.random.default_rng(0)
# 4.000 remuestras del MISMO tamaño, con reemplazo: la muestra hace de población
remuestras = azar.choice(datos, size=(4000, datos.size), replace=True)
medianas = np.median(remuestras, axis=1)
bajo, alto = np.percentile(medianas, [2.5, 97.5])

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.1))

# --- Izquierda: lo unico que se tiene. La media la decide un dato; la mediana no.
orden = np.sort(datos)
ejes[0].plot(orden, np.arange(datos.size), "o", color=AZUL, markersize=7, zorder=3)
ejes[0].axvline(datos.mean(), color=ROJO, linewidth=1.4, linestyle="--")
ejes[0].axvline(np.median(datos), color=VERDE, linewidth=1.4)
anotar(ejes[0], "la mediana, 13,85:\nsiete de los ocho valores\nestán entre 12 y 15",
       xy=(13.85, 4.6), xytext=(0.27, 0.78), color=VERDE)
anotar(ejes[0], "la media, 23,9:\nun solo dato la desplaza",
       xy=(23.9, 1.2), xytext=(0.27, 0.38), color=ROJO)
anotar(ejes[0], "el 96 no es un error de teclado: está en la muestra",
       xy=(96, 7), xytext=(0.28, 0.95), color=TEXTO)
ejes[0].set_xlabel("tiempo de espera (segundos)")
ejes[0].set_ylabel("una fila por llamada")
ejes[0].set_xlim(0, 112)
ejes[0].set_ylim(-0.8, 7.8)
titulo(ejes[0], "La muestra: lo único que tienes",
       "y la única población de la que el bootstrap puede extraer")
rejilla(ejes[0], eje="x")
numeros(ejes[0], ejes="x")

# --- Derecha: las 4.000 medianas. El intervalo sale de los cuantiles, no de una formula.
ejes[1].axvspan(bajo, alto, color=VERDE, alpha=0.12, zorder=0)
ejes[1].hist(medianas, bins=np.arange(12, 16.25, 0.25), color=AZUL, zorder=2)
ejes[1].axvline(np.median(datos), color=ROJO, linewidth=1.4, zorder=3)
ejes[1].axvline(medianas.mean(), color=NARANJA, linewidth=1.4, linestyle=":", zorder=3)
anotar(ejes[1], "el 95 % central:\nde 12,8 a 15,1", xy=(alto, 380), xytext=(0.74, 0.72),
       color=VERDE)
anotar(ejes[1], "la mediana observada, 13,85", xy=(13.85, 700), xytext=(0.03, 0.95),
       color=ROJO)
anotar(ejes[1], "la media de las 4.000 medianas, 14,27:\nel bootstrap se desplaza hacia arriba",
       xy=(medianas.mean(), 700), xytext=(0.03, 0.84), color=NARANJA)
ejes[1].set_xlabel("mediana de cada remuestra (segundos)")
ejes[1].set_ylabel("remuestras (de 4.000)")
ejes[1].set_xlim(11.9, 16.1)
ejes[1].set_ylim(0, 980)
ejes[1].text(0.02, 0.06, "eje recortado: el otro 5 % se reparte entre 12,0 y 96,0;\n"
             "cuando el 96 sale cuatro veces, la mediana se va a 55",
             transform=ejes[1].transAxes, fontsize=8.5, color=TEXTO)
titulo(ejes[1], "Las 4.000 medianas que el bootstrap inventa",
       "su dispersión estima la del muestreo real, que no puedes repetir")
rejilla(ejes[1])
numeros(ejes[1], ejes="x")

guardar(fig, "bootstrap-distribucion-de-la-mediana")
