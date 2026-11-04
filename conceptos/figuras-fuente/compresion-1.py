"""compresion-1.py — de dónde sale el ahorro y hasta dónde se puede apretar.

Izquierda: los códigos que produce Huffman sobre un log repetitivo, símbolo a símbolo,
frente al ideal log₂(1/p) que marca la entropía. La curva real va pegada por encima de la
ideal: el hueco medio es L − H, y la teoría dice que nunca pasa de un bit.
Derecha: el ratio de zlib frente al tamaño de la entrada para tres tipos de datos. En
ficheros pequeños manda la cabecera y comprimir puede hacerlos crecer; los datos
aleatorios no se comprimen nunca, por grandes que sean.
La figura de la página de compresión (fase 10).
"""

import heapq
import itertools
import math
import zlib
from collections import Counter

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


def num(x, dec=2):
    """Números con coma decimal, como se escriben en el portal."""
    return ("%.*f" % (dec, x)).replace(".", ",")


# --- Los datos de la izquierda: un log con la misma estructura en cada línea ----------
lineas = ["2024-03-11T10:{:02d}:{:02d} INFO pedido {:05d} importe {:6.2f} estado {}\n".format(
              i % 60, (i * 7) % 60, 1000 + 13 * i, 5 + (i % 40) * 1.37, "ok" if i % 4 else "error")
          for i in range(240)]
datos = "".join(lineas).encode()

frecuencias = Counter(datos)
n = len(datos)
# La entropía es el suelo: el mínimo de bits por símbolo de cualquier código sin pérdida.
entropia = -sum((c / n) * math.log2(c / n) for c in frecuencias.values())


def huffman(frec):
    """Árbol de Huffman: se unen siempre los dos símbolos menos frecuentes."""
    monticulo = [(p, i, {s: ""}) for i, (s, p) in enumerate(frec.items())]
    heapq.heapify(monticulo)
    desempate = itertools.count(len(monticulo))
    while len(monticulo) > 1:
        p1, _, n1 = heapq.heappop(monticulo)
        p2, _, n2 = heapq.heappop(monticulo)
        for s in n1:
            n1[s] = "0" + n1[s]
        for s in n2:
            n2[s] = "1" + n2[s]
        n1.update(n2)
        heapq.heappush(monticulo, (p1 + p2, next(desempate), n1))
    return monticulo[0][2]


codigos = huffman(frecuencias)
orden = [s for s, _ in frecuencias.most_common()]
largos = np.array([len(codigos[s]) for s in orden], dtype=float)
ideal = np.array([math.log2(n / frecuencias[s]) for s in orden])
media = sum(frecuencias[s] * len(codigos[s]) for s in orden) / n
rango = np.arange(1, len(orden) + 1)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.4))

# --- Izquierda: dónde cae cada código frente al ideal de su frecuencia ---------------
ax = ejes[0]
ax.axhline(8.0, color=NARANJA, linewidth=1.4, linestyle="--")
ax.plot(rango, ideal, color=AZUL, linewidth=1.7, marker="o", markersize=3.2,
        label="ideal de cada símbolo: log₂(1/p)")
ax.step(rango, largos, where="mid", color=VERDE, linewidth=1.9,
        label="bits que le da Huffman")
ax.set_ylim(0.0, 9.8)
anotar(ax, "un código fijo de 8 bits (ASCII)\ngastaría esto en cada símbolo",
       xy=(float(rango[-1]), 8.0), xytext=(0.03, 0.90), color=NARANJA, flecha=False)
anotar(ax, "el símbolo más frecuente es el espacio:\nHuffman le da 3 bits en vez de 8",
       xy=(1.0, float(largos[0])), xytext=(0.04, 0.73), color=VERDE)
anotar(ax, "de media, {} bits por símbolo con Huffman\ny {} con la entropía: el suelo teórico"
       .format(num(media), num(entropia)),
       xy=(3.0, float(ideal[2])), xytext=(0.05, 0.16), color=AZUL)
titulo(ax, "Huffman se pega al suelo de la entropía",
       "bits de cada código, con los {} símbolos ordenados por frecuencia".format(len(orden)))
ax.set_xlabel("símbolos, del más frecuente al menos frecuente")
ax.set_ylabel("bits por símbolo")
ax.legend(loc="upper right", fontsize=8)
rejilla(ax)
numeros(ax, ejes="y")

# --- Derecha: cuánto se aprieta según el tipo de datos y el tamaño -------------------
VOCABULARIO = ("el la de que y en un ser se no haber por con su para como estar tener le lo todo "
               "pero más hacer o poder decir este ir otro ese si me ya ver porque dar cuando muy "
               "sin vez mucho saber sobre mi mismo también hasta ano dos querer entre así primero "
               "desde grande eso ni nos llegar pasar tiempo ella dia uno bien poco deber entonces "
               "poner cosa tanto hombre parecer nuestro tan donde ahora parte después vida quedar "
               "siempre creer hablar llevar dejar nada cada seguir menos nuevo encontrar algo solo "
               "pensar tras").split()
prosa = " ".join(azar.choice(VOCABULARIO, 400_000)).encode()


def ratio(d):
    return 100 * len(zlib.compress(d, 6)) / len(d)


tamanos = np.unique(np.round(np.logspace(1.5, 6.0, 26)).astype(int))
ratios = {
    "log repetitivo": [ratio((b"fila," * (int(t) // 5 + 2))[:int(t)]) for t in tamanos],
    "texto con palabras corrientes": [ratio(prosa[:int(t)]) for t in tamanos],
    "datos aleatorios": [ratio(azar.integers(0, 256, int(t), dtype=np.uint8).tobytes())
                         for t in tamanos],
}

ax = ejes[1]
ax.axhline(100.0, color=REJILLA, linewidth=1.3, linestyle="--")
for valores, color in zip(ratios.values(), [AZUL, VERDE, ROJO]):
    ax.semilogx(tamanos, valores, color=color, linewidth=1.9, marker="o", markersize=3.4)
ax.set_ylim(0.0, 165.0)
anotar(ax, "con menos de 100 bytes manda la cabecera:\nel texto llega a ocupar un {} % más"
       .format(num(max(ratios["texto con palabras corrientes"]) - 100, 0)),
       xy=(float(tamanos[0]), max(ratios["texto con palabras corrientes"])),
       xytext=(0.03, 0.90), color=VERDE)
anotar(ax, "los datos aleatorios se quedan en el 100 %:\nno hay redundancia que quitar",
       xy=(2e5, 100.0), xytext=(0.24, 0.55), color=ROJO)
anotar(ax, "el log, con su estructura repetida,\nbaja al {} %"
       .format(num(ratios["log repetitivo"][-1], 1)),
       xy=(300.0, 8.0), xytext=(0.22, 0.14), color=AZUL)
# Etiquetas directas al final de cada curva: así no hace falta leyenda ni hay que
# buscar el color en el pie.
anotar(ax, "datos aleatorios", xy=(float(tamanos[-1]), 100.0), xytext=(0.97, 0.67),
       color=ROJO, flecha=False, align="right")
anotar(ax, "texto normal", xy=(float(tamanos[-1]), ratios["texto con palabras corrientes"][-1]),
       xytext=(0.97, 0.24), color=VERDE, flecha=False, align="right")
anotar(ax, "log repetitivo", xy=(float(tamanos[-1]), 0.4), xytext=(0.97, 0.06),
       color=AZUL, flecha=False, align="right")
titulo(ax, "Comprimir quita redundancia, no información",
       "tamaño comprimido entre tamaño original, en %, frente al tamaño de la entrada")
ax.set_xlabel("tamaño de la entrada, en bytes")
ax.set_ylabel("ratio, en % (100 = no se ahorra nada)")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "compresion-huffman-y-tope")
