from collections import deque

grafo = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6],
    4: [2, 5],
    5: [2, 4],
    6: [3, 7],
    7: [6],
}

def bfs(grafo, inicio):
    """Devuelve el orden de visita y las distancias en aristas."""
    visitado = {inicio}
    cola = deque([inicio])          # FIFO: lo que entra primero sale primero
    orden, dist = [], {inicio: 0}
    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in grafo[u]:
            if v not in visitado:
                visitado.add(v)     # se marca AL ENCOLAR, no al desencolar
                dist[v] = dist[u] + 1
                cola.append(v)
    return orden, dist

orden, dist = bfs(grafo, 1)
print("orden BFS:", orden)                      # -> orden BFS: [1, 2, 3, 4, 5, 6, 7]
print("distancias:", dist)                      # -> distancias: {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3}
print("distancia a 7:", dist[7])                # -> distancia a 7: 3
