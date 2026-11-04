"""principios-solid-1.py — los dos principios que se ven en números: la promesa que el
subtipo rompe (Liskov) y cuántos ficheros hay que tocar al añadir una variante (OCP).
La figura de la página de principios SOLID (fase 11)."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: el cuadrado rompe la promesa del rectángulo -------------------
casos = [("Rectángulo 2x3\nal que se pone 5 y 4", 20.0, VERDE),
         ("Cuadrado de lado 2\nal que se pone 5 y 4", 16.0, ROJO)]
for i, (etiqueta, area, color) in enumerate(casos):
    ejes[0].bar(i, area, color=color, width=0.55)
    ejes[0].text(i, area + 0.6, "%d" % area, ha="center", fontsize=10, color=TEXTO)

# La línea marca lo que promete el padre: 5 de ancho por 4 de alto son 20.
promesa = 20.0
ejes[0].axhline(promesa, color=TEXTO, linewidth=1.1, linestyle="--")
ejes[0].text(0.62, 23.3, "lo que promete el padre: 20", fontsize=8, color=TEXTO)
ejes[0].set_xticks(range(len(casos)))
ejes[0].set_xticklabels([c[0] for c in casos], fontsize=8)
ejes[0].set_xlim(-0.6, 1.75)
ejes[0].set_ylim(0, 26)
ejes[0].set_ylabel("área tras fijar ancho 5 y alto 4")
titulo(ejes[0], "El mismo contrato, dos resultados",
       "el cuadrado devuelve 16 y no avisa de nada")
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- Derecha: cuántos sitios hay que tocar al añadir una política -------------
politicas = [("Con la cadena de if/elif:\nhay que editar 3 sitios", 3, ROJO),
             ("Con una clase Descuento nueva:\nse editan 0 sitios", 0, VERDE)]
for i, (etiqueta, sitios, color) in enumerate(politicas):
    ejes[1].barh(i, sitios, color=color, height=0.45)
    if sitios:
        ejes[1].text(sitios + 0.08, i, "%d ficheros abiertos" % sitios, va="center",
                     fontsize=8, color=TEXTO)
    else:
        ejes[1].text(0.08, i, "ninguno: se añade una clase y se registra", va="center",
                     fontsize=8, color=TEXTO)

ejes[1].set_yticks(range(len(politicas)))
ejes[1].set_yticklabels([p[0] for p in politicas], fontsize=8)
ejes[1].invert_yaxis()
ejes[1].set_xlim(0, 4.2)
ejes[1].set_xlabel("ficheros que hay que abrir y editar")
titulo(ejes[1], "Añadir una variante: ¿cuántos ficheros tocas?",
       "con if/elif, tres; con una clase nueva, ninguno")
rejilla(ejes[1], "x")
numeros(ejes[1], "x")

guardar(fig, "principios-solid-promesa-y-radio")
