# Backtracking con deshacer sobre un laberinto: 0 = libre, 1 = muro.
laberinto = [
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
]
inicio, fin = (0, 0), (3, 4)

def buscar(celda, camino, visitadas):
    if celda == fin:
        return list(camino)
    fila, col = celda
    for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        f, c = fila + df, col + dc
        if 0 <= f < len(laberinto) and 0 <= c < len(laberinto[0]):
            if laberinto[f][c] == 0 and (f, c) not in visitadas:
                visitadas.add((f, c))
                camino.append((f, c))
                resultado = buscar((f, c), camino, visitadas)
                if resultado:
                    return resultado
                camino.pop()          # callejon sin salida: se deshace
    return None

camino = buscar(inicio, [inicio], {inicio})
print("pasos del camino:", len(camino))     # -> pasos del camino: 8
print("camino:", camino)
# -> camino: [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4)]
