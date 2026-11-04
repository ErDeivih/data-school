import heapq
import itertools
import math
from collections import Counter


def huffman(texto):
    """Codigo libre de prefijo optimo: une siempre los dos simbolos menos frecuentes."""
    contador = itertools.count()          # desempate estable entre frecuencias iguales
    monticulo = [(peso, next(contador), {simbolo: ""})
                 for simbolo, peso in Counter(texto).items()]
    heapq.heapify(monticulo)
    while len(monticulo) > 1:
        p1, _, n1 = heapq.heappop(monticulo)
        p2, _, n2 = heapq.heappop(monticulo)
        for simbolo in n1:
            n1[simbolo] = "0" + n1[simbolo]
        for simbolo in n2:
            n2[simbolo] = "1" + n2[simbolo]
        n1.update(n2)
        heapq.heappush(monticulo, (p1 + p2, next(contador), n1))
    return monticulo[0][2]


texto = "ABRACADABRA"
codigos = huffman(texto)
bits = sum(len(codigos[c]) for c in texto)
entropia = -sum((texto.count(c) / len(texto)) * math.log2(texto.count(c) / len(texto))
                for c in set(texto))

print("codigos:", dict(sorted(codigos.items())))
print("bits con Huffman:", bits)                          # -> 23
print("bits con 3 bits fijos:", 3 * len(texto))           # -> 33
print("entropia: {:.2f} bits/simbolo".format(entropia))   # -> 2.04
print("media Huffman: {:.2f} bits/simbolo".format(bits / len(texto)))  # -> 2.09
