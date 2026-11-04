from collections import deque

# BFS: la cola garantiza que se visita por niveles y no en profundidad.
grafo = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": []}

def bfs(grafo, inicio):
    visitados = {inicio}
    cola = deque([inicio])
    orden, niveles = [], []
    while cola:
        nivel = []
        for _ in range(len(cola)):               # lo que hay en la cola es un nivel completo
            nodo = cola.popleft()
            orden.append(nodo)
            nivel.append(nodo)
            for vecino in grafo[nodo]:
                if vecino not in visitados:      # se marca al encolar, no al desencolar
                    visitados.add(vecino)
                    cola.append(vecino)
        niveles.append(nivel)
    return orden, niveles

print("orden:", bfs(grafo, "A")[0])     # -> orden: ['A', 'B', 'C', 'D', 'E', 'F']
print("niveles:", bfs(grafo, "A")[1])   # -> niveles: [['A'], ['B', 'C'], ['D', 'E'], ['F']]
print("nodos visitados:", len(bfs(grafo, "A")[0]))   # -> nodos visitados: 6
