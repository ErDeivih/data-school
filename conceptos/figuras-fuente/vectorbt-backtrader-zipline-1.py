"""vectorbt-backtrader-zipline-1.py — el mismo universo y la misma regla con los tres modelos
del mundo: arrays, sucesos y corte transversal. La figura de la pagina de VectorBT, Backtrader
y Zipline (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n, activos = 250, 4
# Cuatro activos con una parte comun (el mercado) y una parte propia (lo que los diferencia).
comun = azar.normal(0.0004, 0.008, n)
ret = comun[:, None] + azar.normal(0.0, 0.007, (n, activos))
ret[0] = 0.0
precio = 100 * np.cumprod(1 + ret, axis=0)


def media_movil(w):
    """Media simple de las w barras anteriores, columna a columna."""
    acum = np.vstack([np.zeros((1, precio.shape[1])), np.cumsum(precio, axis=0)])
    return (acum[w:] - acum[:-w]) / w


senal = (precio[19:] > media_movil(20)).astype(float)   # comprado si el cierre supera su media
mercado = ret[20:]            # los retornos que se cobran con la señal de la barra anterior

# --- Vectorizado (estilo VectorBT): la posicion del activo 1 sale de un array desplazado ---
posicion = np.concatenate([[0.0], senal[:-2, 0]])
coste_array = 0.0005 * np.abs(np.diff(posicion, prepend=0.0))
array = posicion * mercado[:, 0] - coste_array

# --- Eventos (estilo Backtrader): la orden llega tarde y se llena solo en parte ---
# El retraso es el mismo desplazamiento, pero aqui ademas la cantidad no es la pedida.
pos_eventos = posicion * 0.85
coste_eventos = 0.0005 * np.abs(np.diff(pos_eventos, prepend=0.0))
eventos = pos_eventos * mercado[:, 0] - coste_eventos

# --- Corte transversal (estilo Zipline): la exposicion sale de seleccionar en cada fecha ---
pesos = senal[:-1] / np.maximum(senal[:-1].sum(axis=1, keepdims=True), 1.0)
exposicion = pesos.sum(axis=1)
coste_pipeline = 0.0005 * np.abs(np.diff(exposicion, prepend=0.0))
pipeline = (pesos * mercado).sum(axis=1) - coste_pipeline

curvas = [
    ("Array desplazado (estilo VectorBT)", np.cumprod(1 + array), AZUL),
    ("Bucle de eventos (estilo Backtrader)", np.cumprod(1 + eventos), VERDE),
    ("Corte transversal (estilo Zipline)", np.cumprod(1 + pipeline), MORADO),
]

fig, ejes = plt.subplots(3, 1, figsize=(7.2, 7.2), sharex=True)

# --- Arriba: array y eventos miran al mismo activo y no coinciden ---
ejes[0].step(np.arange(n - 20), posicion, where="post", color=AZUL, linewidth=1.5)
ejes[0].step(np.arange(n - 20), pos_eventos, where="post", color=VERDE, linewidth=1.5)
ejes[0].set_ylim(-0.05, 1.35)
titulo(ejes[0], "Mismo activo y misma señal: dos ejecuciones",
       "el vectorizado y el motor de eventos dan posiciones distintas")
ejes[0].set_ylabel("exposición")
# Rejillas en 0, 0,5 y 1: con el paso de 0,25 la rejilla de 1,25 partía en dos la nota de
# arriba (medido: 227 px de línea dentro del texto). Por encima de la línea del 1 quedan 48 px,
# sitio de sobra para las dos líneas de la nota, que además ya no se sube hasta el título.
ejes[0].set_yticks([0, 0.5, 1.0])
anotar(ejes[0], "el vectorizado da por hecho el llenado completo; el motor de eventos\n"
                "llega más tarde y solo llena el 85 % de lo pedido",
       xy=(120, 0.85), xytext=(0.03, 0.873), color=NARANJA)
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- En medio: el pipeline no mira una señal, selecciona entre varios activos ---
ejes[1].plot(exposicion, color=MORADO, linewidth=1.6)
ejes[1].axhline(1.0, color=TEXTO, linewidth=0.9, linestyle="--")
ejes[1].set_ylim(0, 1.6)
titulo(ejes[1], "El pipeline reparte el capital entre los elegidos",
       "no compra «sí o no»: cada día decide cuáles de los cuatro")
ejes[1].set_ylabel("activos en cartera")
ejes[1].text(0.03, 0.92, "cada altura es cuántos de los cuatro pasan el filtro ese día;\n"
                         "el capital se reparte a partes iguales entre ellos",
             color=MORADO, fontsize=8.5, va="top", transform=ejes[1].transAxes)
ejes[1].text(0.03, 0.74, "en 0 no hay nada invertido: el filtro deja la cartera fuera del mercado",
             color=REJILLA, fontsize=8.5, va="top", transform=ejes[1].transAxes)
rejilla(ejes[1])
numeros(ejes[1], "y")

# --- Abajo: la consecuencia, que no es un error de ninguno de los tres ---
etiquetas = []
for etiqueta, curva, color in curvas:
    ejes[2].plot(curva, color=color, linewidth=1.7)
    etiquetas.append((float(curva[-1]), etiqueta, color))
# Las tres etiquetas van abajo a la derecha, apiladas y en el mismo orden que las curvas al
# final del eje (la que acaba más baja, abajo). Antes se escribían a la izquierda y a la altura
# final de cada curva: las tres curvas las atravesaban (medido: 35, 16 y 11 px de curva dentro
# del texto de «Bucle de eventos…») y dos de ellas se pisaban entre sí (2,3 px de solape). La
# franja de abajo está vacía porque la curva que más baja no pasa de 0,836.
etiquetas.sort(key=lambda e: e[0])
ejes[2].set_ylim(0.70, 1.06)
for (valor, etiqueta, color), altura in zip(etiquetas, (0.05, 0.13, 0.21)):
    ejes[2].text(0.99, altura, "%s: %.3f" % (etiqueta, valor), color=color, fontsize=8.5,
                 ha="right", va="center", transform=ejes[2].transAxes)
ejes[2].axhline(1.0, color=TEXTO, linewidth=0.8, alpha=0.4)
# La nota de abajo se ha subido al subtítulo: repetía en dos líneas lo mismo que el título.
titulo(ejes[2], "Tres curvas distintas con los mismos datos",
       "la misma regla, tres respuestas según lo que cada motor da por hecho")
ejes[2].set_xlabel("barra")
ejes[2].set_ylabel("capital (empieza en 1)")
rejilla(ejes[2])
numeros(ejes[2], "y")

guardar(fig, "vectorbt-backtrader-zipline-tres-curvas")
