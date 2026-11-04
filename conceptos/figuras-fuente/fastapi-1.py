"""fastapi-1.py — por qué una llamada bloqueante dentro de async def atasca el servicio: el
bucle de eventos atiende una petición detrás de otra. La figura de la página de FastAPI
(fase 11).

El título largo de dos líneas se comía la primera barra, y las dos notas se salían por los
bordes de arriba y de abajo. Ahora el título va corto con su explicación en el subtítulo, y
cada nota vive en una franja vacía: la roja sobre la escalera, la verde a la derecha de las
barras y la naranja en el hueco de arriba a la derecha."""

import numpy as np

from comun import *

estilo()

N = 8               # ocho peticiones a la vez
DURACION = 50       # cada una necesita 50 ms de trabajo
CENTRO_HILOS = (N - 1) / 2                  # fila central del grupo de abajo
CENTRO_BLOQUEO = N + 2 + (N - 1) / 2        # fila central del grupo de arriba

fig, eje = plt.subplots(figsize=(7.8, 4.2))

# Arriba: async def con una llamada bloqueante dentro (un requests.get, un time.sleep o un
# driver síncrono). El bucle no puede soltar la petición, así que las demás hacen cola.
for i in range(N):
    ultima = i == N - 1
    eje.barh(N + 2 + i, DURACION, left=i * DURACION, color=NARANJA if ultima else ROJO,
             height=0.55, alpha=0.85)
# Abajo: def normal (FastAPI la manda a un grupo de hilos) o cliente asíncrono de verdad.
for i in range(N):
    eje.barh(i, DURACION, left=0, color=VERDE, height=0.55, alpha=0.85)

eje.axvline(DURACION, color=TEXTO, linewidth=0.8, linestyle="--", alpha=0.45)
eje.set_yticks([CENTRO_HILOS, CENTRO_BLOQUEO], ["def en un hilo\n(las 8 a la vez)",
                                                "async def con una\nllamada bloqueante"])
# Se estrecha el hueco de en medio y se baja el suelo para que las etiquetas del eje x no
# toquen las barras verdes y las notas quepan enteras dentro del panel.
eje.set_ylim(-1.1, 17.4)
eje.set_xlim(0, 620)
# Nota naranja: en el hueco de arriba a la derecha, por encima de la escalera (que acaba en
# 400 ms) y de la ultima barra (la mas alta, y = 16,3).
eje.text(0.99, 0.95, "la última empieza a los 350 ms\ny acaba a los 400 ms",
         transform=eje.transAxes, ha="right", va="top", fontsize=9, color=NARANJA)
# Nota verde: a la derecha, donde las barras ya han terminado (todas acaban en 50 ms).
eje.text(62, CENTRO_HILOS, "las 8 acaban a los 50 ms", va="center", fontsize=9, color=VERDE)
# Nota roja: la escalera sube de izquierda a derecha, asi que su esquina de arriba a la
# izquierda esta vacia hasta la altura de la ultima barra.
eje.text(0.03, 0.95, "cada petición arranca 50 ms después\ny el bucle no suelta la anterior",
         transform=eje.transAxes, va="top", fontsize=9, color=ROJO)
titulo(eje, "Ocho peticiones de 50 ms, dos formas de atenderlas",
       "si el bucle se bloquea tardan 400 ms; si no, 50 ms")
eje.set_xlabel("milisegundos desde la primera petición")
rejilla(eje, eje="x")
numeros(eje, ejes="x")

guardar(fig, "fastapi-bloqueo-del-bucle")
