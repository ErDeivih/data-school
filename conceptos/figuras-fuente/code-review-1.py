"""code-review-1.py — cuanto se puede revisar de verdad: el diff de 472 lineas contra el limite
de 400, y las dos formas de partirlo hasta que cada trozo se lea de una sentada. La figura de la
pagina de revisión de codigo (fase 11)."""

import numpy as np

from comun import *

estilo()

# El diff del ejemplo de la pagina: tres ficheros, 472 lineas en total.
ficheros = ["src/pagos.py", "tests/test_pagos.py", "CHANGELOG.md"]
lineas = np.array([320, 140, 12])
LIMITE = 400

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 4.2))

# --- Izquierda: como se compone el diff y donde cae el limite ----------------------
# Barra apilada en una sola fila: los tramos suman el total y el sobrante se ve de un golpe.
izquierda = 0
colores = [AZUL, VERDE, NARANJA]
# Etiquetas cortas dentro de cada tramo: el nombre completo ya va en la leyenda.
rotulos = ["pagos.py", "tests", "CHANGELOG"]
centros = []
for fichero, n, color in zip(ficheros, lineas, colores):
    izq.barh(0, n, left=izquierda, color=color, height=0.5, label=f"{fichero} ({n})")
    centros.append(izquierda + n / 2)
    izquierda += n
# Solo se rotula el tramo si es ancho: en 12 lineas el texto se saldria de la barra. El rotulo
# se aparta del centro geometrico cuando ahi cae la raya del limite (en 400): el tramo de pruebas
# va de 320 a 460 y su centro cae justo encima de la raya, que si no tacha el texto.
desplazamiento = {1: -25}
posiciones = [c + desplazamiento.get(i, 0) for i, c in enumerate(centros)]
for posicion, n, corto in zip(posiciones, lineas, rotulos):
    if n > 40:
        izq.text(posicion, 0, corto, ha="center", va="center", color="white", fontsize=8)
# Una linea fina senala el tramo mas estrecho (las 12 lineas del CHANGELOG), que va sin rotulo.
# Cae en el hueco que queda entre ese tramo y la raya del limite, sin pisar las barras.
izq.plot([470, 470], [0.06, 0.20], color=TEXTO, linewidth=0.8)
# La linea del limite marca las 400 lineas: todo lo que queda a la derecha no se revisa.
# Se queda por encima de la franja de abajo para no tachar el texto de aviso.
izq.axvline(LIMITE, color=ROJO, linewidth=1.6, linestyle="--", ymin=0.36)
# Los dos avisos van en las franjas vacias: arriba a la derecha del limite y debajo de la barra.
anotar(izq, "límite: 400 líneas", xy=(LIMITE, 0.52), xytext=(0.74, 0.86), color=ROJO)
# La flecha entra desde abajo a la izquierda del tramo: asi no cruza ningun rotulo de la barra.
anotar(izq, "las 12 líneas del CHANGELOG\nquedan fuera: nadie las lee",
       xy=(462, -0.16), xytext=(0.40, 0.12), color=ROJO)
izq.set_xlim(0, 560)
izq.set_ylim(-0.75, 0.75)
izq.set_yticks([])
izq.set_xlabel("lineas cambiadas en el diff")
titulo(izq, "472 líneas de diff contra un límite de 400",
       "lo que pasa del límite se aprueba sin leer")
izq.legend(loc="upper center", ncols=1, bbox_to_anchor=(0.5, -0.30))
rejilla(izq, eje="x")
numeros(izq)

# --- Derecha: partirlo hasta que cada trozo quepa -----------------------------------
propuestas = ["de una vez\n(472 lineas)", "partido en 2\n(320 + 152)", "partido en 3\n(220 + 140 + 112)"]
maximos = [472, 320, 220]
colores_der = [ROJO, NARANJA, VERDE]
barras = der.bar(propuestas, maximos, color=colores_der, width=0.5)
der.bar_label(barras, labels=[f"{m}" for m in maximos], padding=3, fontsize=9)
der.axhline(LIMITE, color=TEXTO, linewidth=1.2, linestyle="--")
# El rotulo va justo ENCIMA de la raya: a la altura de la linea el texto la cortaba por la mitad.
der.text(2.30, LIMITE + 18, "límite 400", color=TEXTO, fontsize=9, ha="right")
der.set_ylim(0, 560)
der.set_ylabel("lineas del trozo más grande")
titulo(der, "Partir el cambio lo hace revisable",
       "ningún trozo pasa de 400 líneas")
rejilla(der)
# Solo el eje y: el eje x lleva nombres de texto, no numeros.
numeros(der, ejes="y")

guardar(fig, "code-review-tamano-del-diff")
