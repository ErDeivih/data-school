"""errores-y-depuracion-1.py - que se traga de verdad un except sin tipo declarado cuando la
cadena de limpieza tiene un fallo de programación. La figura de la pagina de errores y
depuración (fase 3)."""

import numpy as np

from comun import *

estilo()
fig, ax = plt.subplots(figsize=(7.4, 3.4))

# 20000 filas: el 12 % trae texto donde deberia haber un numero
azar = np.random.default_rng(5)
n = 20_000
malas = int((azar.random(n) < 0.12).sum())


def limpia_fila(texto):
    """Convierte el texto de una celda en número."""
    return float(texto)


# 1) except sin tipo: perdona el dato malo Y el fallo de programacion
rechazadas, tragadas = 0, 0
for _ in range(malas):
    try:
        limpia_fila("doce")
    except:                       # no dice que espera: lo perdona todo
        rechazadas += 1
try:
    limpia_fila(None)             # falta la comprobacion: es un fallo de programacion
except:
    tragadas += 1

# 2) except con el tipo concreto: el dato malo se marca y el fallo de programacion sube
marcadas = 0
for _ in range(malas):
    try:
        limpia_fila("doce")
    except ValueError:            # solo el error que se sabe manejar
        marcadas += 1
try:
    limpia_fila(None)
except TypeError:
    print("el fallo de programación se ve y se puede arreglar")

sin_tipo = [rechazadas, tragadas, n - rechazadas - tragadas]
con_tipo = [marcadas, 0, n - marcadas]

y = np.arange(2)
alto = 0.34
ax.barh(y + alto / 2, sin_tipo[0], height=alto, color=VERDE)
ax.barh(y + alto / 2, sin_tipo[1], height=alto, left=sin_tipo[0], color=ROJO)
ax.barh(y + alto / 2, sin_tipo[2], height=alto, left=sin_tipo[0] + sin_tipo[1], color=NARANJA)
ax.barh(y - alto / 2, con_tipo[0], height=alto, color=VERDE)
ax.barh(y - alto / 2, con_tipo[1], height=alto, left=con_tipo[0], color=ROJO)
ax.barh(y - alto / 2, con_tipo[2], height=alto, left=con_tipo[0] + con_tipo[1], color=NARANJA)

ax.set_yticks(y, ["except: sin tipo", "except ValueError:"])
titulo(ax, "El except sin tipo también perdona el fallo de programación")
ax.set_xlabel("filas de 20000 que acaban en cada estado")
# El tramo rojo mide una fila de 20000: invisible a esta escala. Se marca desde la banda
# vacia de arriba con una linea, y las dos etiquetas van dentro de su tramo verde.
ax.set_ylim(-0.15, 2.75)
ax.annotate("fallo oculto: 1 fila", xy=(rechazadas / 2, 1.55), xytext=(rechazadas / 2, 2.55),
            color=ROJO, fontsize=8.5, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color=ROJO, linewidth=0.9))
ax.text(400, 1.98, "1 oculta", color=TEXTO, fontsize=8.5, va="center", ha="left")
ax.text(400, 0.62, "1 marcada", color=TEXTO, fontsize=8.5, va="center", ha="left")
ax.text(0.0, -0.19, "verde: dato malo rechazado   naranja: pasa sin revisar",
        transform=ax.transAxes, color=TEXTO, fontsize=8.5, va="top", ha="left")
rejilla(ax, eje="x")
numeros(ax, "x")
guardar(fig, "errores-y-depuracion-except-sin-tipo")