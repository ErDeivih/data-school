"""coste-y-latencia-1.py — de qué está hecha la factura de una consulta y de qué está hecha
su espera. La figura de la página de coste y latencia (fase 8)."""

import numpy as np
from matplotlib.transforms import blended_transform_factory

from comun import *

estilo()

# Los precios y el modelo de latencia son los de la página: euros por millón de tokens.
P_ENTRADA, P_CACHE, P_SALIDA = 3.0, 0.30, 15.0
SISTEMA, HISTORIAL, SALIDA = 3000, 12000, 300
T0, A_ENTRADA, A_CACHE, B_SALIDA = 50.0, 0.002, 0.0002, 20.0


def coste(documentos, con_cache):
    """Euros por consulta con `documentos` tokens recuperados."""
    prefijo = SISTEMA + HISTORIAL
    if con_cache:
        return (documentos * P_ENTRADA + prefijo * P_CACHE + SALIDA * P_SALIDA) / 1e6
    return ((prefijo + documentos) * P_ENTRADA + SALIDA * P_SALIDA) / 1e6


def latencia(entrada, cache_aciertos):
    """(primer token, total) en milisegundos para esa entrada."""
    ttft = T0 + (entrada - cache_aciertos) * A_ENTRADA + cache_aciertos * A_CACHE
    return ttft, ttft + SALIDA * B_SALIDA


# Dos paneles en DOS filas y no en una: en una fila el panel del coste se queda en la mitad
# de ancho (las etiquetas largas del panel derecho se comen el sitio) y los rótulos se salían
# del eje. En dos filas cada panel usa todo el ancho.
fig, ejes = plt.subplots(2, 1, figsize=(8.6, 7.2))

# --- Izquierda: qué mueve el coste por consulta -------------------------------
miles = np.linspace(0, 120, 240)                                # de 0 a 120.000 tokens de documentos
ejes[0].plot(miles, coste(miles * 1000, False), color=AZUL, linewidth=1.8, label="sin caché")
ejes[0].plot(miles, coste(miles * 1000, True), color=VERDE, linewidth=1.8,
             label="con caché del prefijo estable")

# Los tres puntos que discute la página. Cada rótulo va en un hueco medido, no a ojo: la recta
# verde recorre todo el ancho, así que solo deja libre la franja de arriba; dentro de ella, el
# rojo (el más largo) va abajo a la derecha, el morado encima y el naranja, que es el más corto,
# abajo a la izquierda. Comprobado midiendo en px: 0 cruces de recta dentro de las tres cajas.
# El rojo se separa del borde para que su flecha no le pase por encima del texto.
puntos = [
    (120, False, ROJO, "120.000 sin caché: 0,409 €", (0.55, 0.855)),
    (120, True, MORADO, "los mismos con caché: 0,369 €", (0.60, 0.975)),
    (30, True, NARANJA, "recortando: 0,099 €", (0.02, 0.755)),
]
for docs, con_cache, color, texto, pos in puntos:
    y = coste(docs * 1000, con_cache)
    ejes[0].plot([docs], [y], marker="o", markersize=5, color=color)
    align = "right" if pos[0] > 0.5 else "left"
    anotar(ejes[0], texto, xy=(docs, y), xytext=pos, color=color, align=align)

ejes[0].set_xlabel("miles de tokens de documentos recuperados")
ejes[0].set_ylabel("euros por consulta")
# El eje no llega a cero, así que el localizador automático se inventaba un «-0,05» que caía
# encima del «-20» del eje x (medido: y=367..381 contra y=357..371). Con la lista de ticks
# escrita a mano no hay ninguno negativo.
ejes[0].set_ylim(-0.01, 0.44)
ejes[0].set_yticks([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
titulo(ejes[0], "El coste lo decide cuántos documentos entran",
       "la caché solo abarata el prefijo que se repite")
# La leyenda baja a la esquina de abajo a la derecha: arriba compartía franja con los rótulos
# y su etiqueta quedaba tachada. Con el marco transparente, la recta que pasa por detrás se
# sigue viendo.
ejes[0].legend(loc="lower right", framealpha=0.0)
rejilla(ejes[0])
numeros(ejes[0])

# --- Derecha: qué mueve la espera ---------------------------------------------
casos = [
    ("contexto corto: 4.000 de entrada", 4000, 0),
    ("contexto largo: 120.000 de entrada", 120000, 0),
    ("contexto largo con 115.000 en caché", 120000, 115000),
]
# Los milisegundos de cada barra se escriben en una columna fija a la derecha del eje: dentro
# no caben (el texto salía por encima de la barra larga y del borde del panel).
columna = blended_transform_factory(ejes[1].transAxes, ejes[1].transData)
for i, (etiqueta, entrada, cache) in enumerate(casos):
    ttft, total = latencia(entrada, cache)
    color = AZUL if cache == 0 else VERDE
    ejes[1].barh(i, ttft, color=color, height=0.55)
    ejes[1].text(1.03, i, f"{ttft:.0f} ms   (el total son {total:.0f} ms)",
                 transform=columna, va="center", ha="left", fontsize=8, color=TEXTO)

ejes[1].set_yticks(range(len(casos)))
ejes[1].set_yticklabels([c[0] for c in casos], fontsize=8)
ejes[1].invert_yaxis()                                          # el primer caso, arriba
ejes[1].set_xlim(0, 320)
ejes[1].set_xlabel("milisegundos hasta la primera palabra")
titulo(ejes[1], "Los tres casos terminan casi a la vez",
       "lo único que cambia es el primer token")
rejilla(ejes[1], "x")
numeros(ejes[1], "x")

guardar(fig, "coste-y-latencia-factura-y-espera")
