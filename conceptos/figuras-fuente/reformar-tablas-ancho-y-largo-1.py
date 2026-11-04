"""reformar-tablas-ancho-y-largo-1.py — cuánto crece la tabla al pasar de ancha a larga y qué
pasa con los huecos al deshacer el camino. Figura de la página reformar-tablas-ancho-y-largo
(fase 3)."""

import numpy as np

from comun import *

estilo()

clientes = 500
meses = np.arange(1, 13)
filas_larga = clientes * meses

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.4))

ejes[0].plot(meses, filas_larga, color=AZUL, linewidth=1.8, marker="o", markersize=3.5,
             label="tabla larga: clientes · meses")
ejes[0].plot(meses, np.full_like(meses, clientes, dtype=float), color=ROJO, linewidth=1.8,
             label="tabla ancha: una fila por cliente")
ejes[0].set_ylim(0, 7000)
ejes[0].set_xlabel("columnas de meses en la tabla ancha")
ejes[0].set_ylabel("filas de la tabla")
ejes[0].set_xticks(meses)
ejes[0].legend(loc="upper left")
titulo(ejes[0], "La tabla larga paga una fila por variable",
       "500 clientes: la ancha no cambia de filas, la larga se multiplica por 12")
anotar(ejes[0], "12 meses: 6.000 filas largas", xy=(12, 6000), xytext=(0.42, 0.68), color=AZUL)
rejilla(ejes[0])
numeros(ejes[0])

etiquetas = ["tabla larga\ncompleta", "a la larga\nle faltan 3 pares"]
con_dato = [12, 9]
huecos = [0, 3]
ejes[1].bar(etiquetas, con_dato, color=AZUL, width=0.5, label="celdas con dato")
ejes[1].bar(etiquetas, huecos, bottom=con_dato, color=NARANJA, width=0.5, label="celdas NaN")
ejes[1].set_ylim(0, 15)
ejes[1].set_xlim(-0.65, 1.65)
ejes[1].set_ylabel("celdas del pivote")
ejes[1].legend(loc="upper left")
titulo(ejes[1], "El pivote devuelve el producto cartesiano",
       "los pares que faltaban en la tabla larga vuelven como NaN")
anotar(ejes[1], "3 celdas vuelven vacías", xy=(1.28, 12.2), xytext=(0.40, 0.88), color=NARANJA)
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "reformar-tablas-ancho-y-largo-celdas")
