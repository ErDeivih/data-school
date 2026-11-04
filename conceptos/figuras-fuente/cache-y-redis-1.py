"""cache-y-redis-1.py — de qué depende la tasa de aciertos y por qué la latencia media la
decide el porcentaje que falla. La figura de la página de caché y Redis (fase 11)."""

import numpy as np

from collections import OrderedDict

from comun import *

estilo()

K = 2000          # claves distintas en el catálogo
N = 20000         # peticiones simuladas
capacidades = np.unique(np.round(np.geomspace(10, K, 12)).astype(int))
rng = np.random.default_rng(5)


def flujo(exponente):
    """Peticiones con distribución zipf: exponente grande = pocas claves se llevan casi todo."""
    valores = []
    while len(valores) < N:
        z = rng.zipf(exponente, N)
        valores.extend(z[z <= K].tolist())        # fuera del catálogo se descartan
    return np.array(valores[:N]) - 1


def tasa_de_acierto(claves, capacidad):
    """Simula la caché LRU del código de la página y devuelve la fracción de aciertos."""
    cache = OrderedDict()
    aciertos = 0
    for c in claves:
        if c in cache:
            cache.move_to_end(c)                  # lo usado va al final: es el criterio LRU
            aciertos += 1
        else:
            cache[c] = True
            if len(cache) > capacidad:
                cache.popitem(last=False)         # se tira el primero, el menos usado
    return aciertos / len(claves)


concentrada = flujo(1.8)
plana = flujo(1.1)

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 3.9))

# --- Izquierda: la tasa de aciertos depende de la demanda, no solo del tamaño ---------
for nombre, claves, color in [("demanda concentrada (zipf 1,8)", concentrada, VERDE),
                              ("demanda plana (zipf 1,1)", plana, ROJO)]:
    tasas = [tasa_de_acierto(claves, int(c)) for c in capacidades]
    izq.plot(capacidades / K, tasas, color=color, linewidth=1.8, marker="o", markersize=3,
             label=nombre)
izq.axhline(0.8, color=TEXTO, linewidth=1.1, linestyle="--")
izq.text(0.46, 0.66, "80 %: por debajo, algo va mal", fontsize=9, color=TEXTO)
izq.set_ylim(0, 1.04)
izq.set_xlim(0, 1.03)
izq.set_xlabel("parte del catálogo que cabe en memoria")
izq.set_ylabel("tasa de aciertos")
titulo(izq, "10 claves de 2.000 ya dan más del 80 %",
       "con la demanda concentrada; con la plana hacen falta 500")
izq.legend(loc="lower right")
rejilla(izq)
numeros(izq)

# --- Derecha: la latencia media la fija lo que falla ---------------------------------
acierto_ms, fuente_ms = 1.0, 200.0
h = np.linspace(0, 1, 101)
# El viaje a la caché se paga siempre; solo los aciertos se ahorran la consulta cara.
media = h * acierto_ms + (1 - h) * (fuente_ms + acierto_ms)
der.plot(h, media, color=AZUL, linewidth=1.8)
der.axhline(fuente_ms, color=TEXTO, linewidth=1.1, linestyle="--")
der.text(0.02, fuente_ms + 7, "sin caché: 200 ms por lectura", fontsize=9, color=TEXTO)
for tasa, color in [(0.80, ROJO), (0.95, NARANJA)]:
    der.scatter([tasa], [tasa * acierto_ms + (1 - tasa) * (fuente_ms + acierto_ms)],
                color=color, zorder=3)
# Las dos notas van en el hueco que deja la propia recta azul y centradas entre dos renglones de
# la rejilla (cada 25 ms): antes la recta las atravesaba y la raya de 175 pasaba por el texto.
anotar(der, "80 % de aciertos → 41 ms", xy=(0.80, 41), xytext=(0.30, 0.74), color=ROJO)
anotar(der, "95 % de aciertos → 11 ms", xy=(0.95, 11), xytext=(0.42, 0.15), color=NARANJA)
der.set_xlim(0, 1.02)
der.set_ylim(0, 220)
der.set_xlabel("tasa de aciertos")
der.set_ylabel("latencia media por lectura (ms)")
titulo(der, "El que falla manda en la latencia media",
       "con un 80 % de aciertos la media es 41 ms, no 1 ms")
rejilla(der)
numeros(der)

guardar(fig, "cache-aciertos-y-coste")
