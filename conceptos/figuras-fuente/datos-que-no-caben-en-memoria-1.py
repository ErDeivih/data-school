"""datos-que-no-caben-en-memoria-1.py — el pico de memoria de leer un fichero entero frente a
leerlo por bloques, y por qué la media de medias no es la media. Figura de la página
datos-que-no-caben-en-memoria (fase 3)."""

import numpy as np

from comun import *

estilo()

bytes_por_fila = 3 * 8                              # tres columnas numericas de 8 bytes
millones = np.linspace(0, 400, 200)                 # millones de filas del fichero
gb_completo = millones * 1e6 * bytes_por_fila / 1e9
gb_bloque = 100_000 * bytes_por_fila / 1e9          # 100.000 filas: siempre lo mismo
ram = 8.0                                           # memoria del portatil, en GB

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.4))

ejes[0].plot(millones, gb_completo, color=ROJO, linewidth=1.8, label="lectura completa")
ejes[0].plot(millones, np.full_like(millones, gb_bloque), color=AZUL, linewidth=1.8,
             label="por bloques (100.000 filas)")
ejes[0].axhline(ram, color=TEXTO, linewidth=1.0, linestyle="--", alpha=0.55)
ejes[0].set_ylim(0, 10.5)
ejes[0].set_xlabel("filas del fichero (millones)")
ejes[0].set_ylabel("memoria (GB)")
ejes[0].legend(loc="upper left")
titulo(ejes[0], "La lectura completa crece con el fichero",
       "el bloque ocupa lo mismo con 1 millón de filas que con 400")
# La nota del cruce va en el hueco de arriba a la izquierda, por debajo de la leyenda y por
# encima de la recta roja: mas a la derecha o mas abajo, la propia recta la atravesaba.
anotar(ejes[0], "333 millones de filas ya no caben en 8 GB", xy=(333, ram), xytext=(0.05, 0.62),
       color=ROJO)
# La nota del bloque va debajo de su linea, en el hueco que queda entre esa linea y el eje: un
# poco mas arriba, la linea de la rejilla del 2 le rozaba la base del texto.
anotar(ejes[0], "el bloque ocupa siempre lo mismo", xy=(230, gb_bloque), xytext=(0.34, 0.13),
       color=AZUL)
rejilla(ejes[0])
numeros(ejes[0])

bloques = [10.0, 10.0, 28.0]                        # medias de bloques de 7.500 filas
ejes[1].bar(["bloque 1", "bloque 2", "bloque 3"], bloques, color=AZUL, width=0.55)
ejes[1].axhline(14.5, color=ROJO, linewidth=1.4, linestyle="--", label="media real: 14,5")
ejes[1].axhline(16.0, color=MORADO, linewidth=1.4, linestyle=":", label="media de las medias: 16,0")
ejes[1].set_ylim(0, 40)
ejes[1].set_ylabel("media del importe")
ejes[1].legend(loc="upper left")
titulo(ejes[1], "La media de medias no es la media",
       "20.000 importes: 19.000 valen 10 y 1.000 valen 100")
anotar(ejes[1], "se desvía 1,5 hacia arriba", xy=(2.30, 15.3), xytext=(0.42, 0.62), color=MORADO)
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "datos-que-no-caben-en-memoria-bloques")
