"""ventanas-de-contexto-1.py — la memoria de la cache KV: lineal con los tokens y
multiplicada por la concurrencia. La figura de la pagina de contexto (fase 8)."""

import numpy as np

from comun import *

estilo()

CAPAS, CABEZAS, DIM, BYTES = 32, 8, 128, 2


def cache_mib(tokens, secuencias=1):
    """La cuenta de la pagina, en MiB: 2 tensores por capa y cabeza, y 2 bytes por valor."""
    return 2 * CAPAS * CABEZAS * DIM * tokens * BYTES * secuencias / 1024 ** 2


fig, ejes = plt.subplots(1, 2, figsize=(8.4, 4.0))   # mas alta: los titulos llevan subtitulo

# --- Panel izquierdo: una secuencia contra treinta y dos ---------------------
ejemplo = [4096, 8192, 32768]
pos = np.arange(3)
ancho = 0.38
una = [cache_mib(t) for t in ejemplo]
treinta = [cache_mib(t, 32) for t in ejemplo]

ejes[0].bar(pos - ancho / 2, una, width=ancho, color=AZUL, label="1 petición")
ejes[0].bar(pos + ancho / 2, treinta, width=ancho, color=ROJO, label="32 peticiones a la vez")

for i, (u, t) in enumerate(zip(una, treinta)):
    ejes[0].text(i - ancho / 2, u + 1200, f"{u:,.0f}".replace(",", "."), ha="center", fontsize=8, color=AZUL)
    ejes[0].text(i + ancho / 2, t + 1200, f"{t:,.0f}".replace(",", "."), ha="center", fontsize=8, color=ROJO)

# La nota va en coordenadas del eje (0-1), en la franja que queda libre entre la leyenda y
# las barras bajas, con el texto pegado a su derecha para que la flecha salga hacia la barra
# roja del ultimo grupo sin cruzarlo.
anotar(ejes[0], "la cache es por secuencia: 32 usuarios\nmultiplican la memoria por 32",
       xy=(2.0, 120000), xytext=(0.72, 0.55), color=ROJO, align="right")
ejes[0].set_xticks(pos)
ejes[0].set_xticklabels([f"{t:,}".replace(",", ".") for t in ejemplo], fontsize=9)
ejes[0].set_xlabel("tokens en el contexto")
ejes[0].set_ylabel("memoria de la cache KV (MiB)")
ejes[0].set_ylim(0, 168000)
ejes[0].set_yticks([0, 40000, 80000, 120000, 160000])
titulo(ejes[0], "La cache crece con los tokens", "y se multiplica por quien pregunta a la vez")
ejes[0].legend(loc="upper left")
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel derecho: el trabajo de atencion crece al cuadrado ------------------
n = np.logspace(2, 4.5, 120)
trabajo = n ** 2
ejes[1].loglog(n, trabajo, color=MORADO, linewidth=1.8)
for base in (4096, 32768):
    ejes[1].plot([base], [base ** 2], "o", color=NARANJA, markersize=6)
# Las dos notas van en coordenadas del eje (0-1) para caer en los dos triangulos que deja la
# recta y = n^2, que en log-log es la diagonal del panel. La de la pendiente cabe arriba a la
# izquierda (queda por encima de la diagonal); la del salto de longitud NO: a esa altura la
# diagonal la cruzaba por la mitad. Va abajo a la derecha, con el texto pegado a su borde
# derecho para no salirse y con la flecha subiendo por el margen hasta el punto naranja.
anotar(ejes[1], "x8 de longitud, x64 de trabajo",
       xy=(32768, 32768 ** 2), xytext=(0.97, 0.10), color=MORADO, align="right")
pendiente = np.polyfit(np.log(n), np.log(trabajo), 1)[0]
anotar(ejes[1], f"pendiente en escala log: {pendiente:.2f}".replace(".", ","),
       xy=(1000, 1000 ** 2), xytext=(0.05, 0.88), flecha=False)
ejes[1].set_xlabel("tokens n (escala logaritmica)")
ejes[1].set_ylabel("comparaciones de atención")
titulo(ejes[1], "Duplicar el contexto cuadruplica el trabajo",
       "lo largo se paga en tiempo y en dinero")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "ventanas-cache-kv-y-coste-cuadratico")
