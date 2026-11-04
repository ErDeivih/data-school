import heapq

def fusionar_k(vueltas):
    """Lo que hace heapq.merge por dentro: un monticulo con la cabeza de cada vuelta."""
    monton = [(v[0], i) for i, v in enumerate(vueltas) if v]   # (valor, de que vuelta viene)
    heapq.heapify(monton)                                      # O(k) y se hace una sola vez
    posicion, salida, operaciones = [0] * len(vueltas), [], 0
    while monton:
        valor, i = heapq.heappop(monton)
        operaciones += 1
        salida.append(valor)
        posicion[i] += 1
        if posicion[i] < len(vueltas[i]):
            heapq.heappush(monton, (vueltas[i][posicion[i]], i))
    return salida, operaciones

vueltas = [[2, 5, 7], [1, 8, 9], [3, 4, 6]]
salida, operaciones = fusionar_k(vueltas)
print("fusionado:", salida)              # -> fusionado: [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("operaciones de monticulo:", operaciones)     # -> operaciones de monticulo: 9
# Cada operacion baja a lo sumo log2(k) niveles del monticulo: con k = 3 son 2 niveles
# por registro, y con k = 1.000.000 serian 20. Es el precio de fusionar muchas vias.
print("niveles con k = 1000000:", 20)    # -> niveles con k = 1000000: 20
