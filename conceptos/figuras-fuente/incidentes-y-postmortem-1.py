"""incidentes-y-postmortem-1.py — la linea de tiempo de un incidente: lo que se tarda en
enterarse, lo que se tarda en parar el dano y lo que ve el usuario. La figura de la pagina de
incidentes y postmortem (fase 11)."""

import numpy as np

from comun import *

estilo()

# Los hitos del ejemplo de la pagina, en minutos desde el despliegue de las 02:55.
despliegue, inicio, deteccion, mitigacion, restauracion = 0, 7, 10, 45, 75
# El mismo fallo declarado SEV3: nadie esta de guardia, se arregla a lo largo de la manana.
sev3_inicio, sev3_mitigacion, sev3_restauracion = 7, 111, 128

fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(9.6, 6.4))

# --- Arriba: los hitos sobre una sola linea -----------------------------------------
arriba.hlines(0, -8, restauracion + 12, color=REJILLA, linewidth=0.9)
# La franja roja empieza en el fallo real, no en la deteccion: es el dano que sufre el cliente.
arriba.axvspan(inicio, mitigacion, color=ROJO, alpha=0.12, linewidth=0)
arriba.axvspan(mitigacion, restauracion, color=VERDE, alpha=0.10, linewidth=0)

hitos = [
    (despliegue, "02:55\nse despliega", REJILLA, 0.40, "left"),
    # 03:02 y 03:05 caen a tres minutos: las etiquetas van a alturas distintas para no pisarse.
    (inicio, "03:02\nempieza a fallar", NARANJA, 0.40, "left"),
    (deteccion, "03:05\nalerta", AZUL, 0.84, "left"),
    (mitigacion, "03:40\nse revierte", VERDE, 0.40, "center"),
    (restauracion, "04:10\nestable", MORADO, 0.40, "right"),
]
for x, texto, color, altura, alineacion in hitos:
    arriba.plot([x], [0], marker="o", color=color, markersize=7, zorder=3)
    arriba.text(x, altura, texto, ha=alineacion, va="center", fontsize=8.5, color=color)

# Los dos tramos que no se pueden separar: avisar y parar el dano.
arriba.annotate("", xy=(deteccion, -0.34), xytext=(inicio, -0.34),
                arrowprops=dict(arrowstyle="<->", color=NARANJA, linewidth=0.9))
arriba.text((inicio + deteccion) / 2, -0.48, "MTTD\n3 min", ha="center", va="top", fontsize=8.5,
            color=NARANJA)
arriba.annotate("", xy=(mitigacion, -0.34), xytext=(deteccion, -0.34),
                arrowprops=dict(arrowstyle="<->", color=AZUL, linewidth=0.9))
arriba.text((deteccion + mitigacion) / 2, -0.48, "MTTM\n35 min", ha="center", va="top", fontsize=8.5,
            color=AZUL)
# La llave del impacto va por debajo de todo: es la cifra que ve quien paga.
arriba.annotate("", xy=(restauracion, -0.78), xytext=(inicio, -0.78),
                arrowprops=dict(arrowstyle="<->", color=ROJO, linewidth=1.1))
arriba.text((inicio + restauracion) / 2, -0.90, "impacto: 68 minutos de peticiones fallando",
            ha="center", va="top", fontsize=9, color=ROJO)

arriba.set_ylim(-1.35, 1.05)
arriba.set_yticks([])
arriba.set_xlim(-8, 92)
arriba.set_xlabel("minutos desde el despliegue")
titulo(arriba, "El impacto empieza antes de que nadie lo sepa",
       "revertir a las 03:10 habria dejado el impacto en 8 minutos")
rejilla(arriba, eje="x")

# --- Abajo: la misma averia, contada segun quien la sufre ---------------------------
filas = ["SEV2: alerta y\nturno de guardia", "SEV3: sin alerta,\nse arregla de dia"]
inicios = [inicio, sev3_inicio]
mitigaciones = [mitigacion, sev3_mitigacion]
restauraciones = [restauracion, sev3_restauracion]
colores = [VERDE, ROJO]
alturas = [0.0, 1.15]          # separacion entre las dos filas, para que quepa la nota de en medio

for i, (ini, mit, res, color, y) in enumerate(zip(inicios, mitigaciones, restauraciones, colores,
                                                  alturas)):
    dano = mit - ini
    # El tramo oscuro es el dano nuevo; el claro, el trabajo de fondo ya sin clientes sufriendo.
    abajo.barh(y, dano, left=ini, color=color, height=0.30)
    abajo.barh(y, res - mit, left=mit, color=color, height=0.30, alpha=0.28)
    # Las dos etiquetas van alineadas en una columna a la derecha de todas las barras: dentro de
    # la barra o pegadas a su final se solapan con la siguiente fila.
    abajo.text(142, y, "%d min de dano" % dano, va="center", fontsize=8.5, color=color)

anotar(abajo, "el mismo fallo, tres veces más dano", xy=(sev3_mitigacion - 22, 0.55),
       xytext=(0.54, 0.60), color=ROJO, flecha=False)
anotar(abajo, "el tramo claro ya no hace dano:\nes trabajo de fondo", xy=(restauracion, 0.15),
       xytext=(0.22, 0.93), color=VERDE)
abajo.set_yticks(alturas)
abajo.set_yticklabels(filas, fontsize=8.5)
abajo.set_ylim(-0.55, 1.75)
abajo.set_xlim(-8, 180)
abajo.set_xlabel("minutos desde el despliegue")
titulo(abajo, "Declarar la gravedad a la baja alarga el dano",
       "la alerta no cambia el fallo, cambia cuando se arregla")
rejilla(abajo, eje="x")

guardar(fig, "incidentes-linea-de-tiempo")
