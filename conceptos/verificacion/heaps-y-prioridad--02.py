import heapq

# Los 3 precios mas altos de un flujo de 1.000.000 de valores, con 3 huecos de memoria.
# El truco: un MIN-heap de tamano k; la raiz es el peor de los que llevas.
def top_k(flujo, k):
    monton = []
    for x in flujo:
        if len(monton) < k:
            heapq.heappush(monton, x)
        elif x > monton[0]:          # solo entra si mejora al peor de los elegidos
            heapq.heapreplace(monton, x)
    return sorted(monton, reverse=True)

import random
rng = random.Random(0)               # semilla fija: el resultado es reproducible
flujo = [rng.randrange(1_000_000) for _ in range(1_000_000)]
print("top 3:", top_k(flujo, 3))     # -> top 3: [999999, 999997, 999996]
