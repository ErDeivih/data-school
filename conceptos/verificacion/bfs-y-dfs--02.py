grafo = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6],
    4: [2, 5],
    5: [2, 4],
    6: [3, 7],
    7: [6],
}

def dfs_iterativo(grafo, inicio):
    """DFS con pila explicita: sin recursion, sin riesgo de desbordar."""
    visitado = {inicio}
    pila = [inicio]                 # LIFO: lo ultimo que entro sale primero
    orden = []
    while pila:
        u = pila.pop()
        orden.append(u)
        for v in reversed(grafo[u]):   # reversed para respetar el orden de los vecinos
            if v not in visitado:
                visitado.add(v)
                pila.append(v)
    return orden

def dfs_recursivo(grafo, u, visitado, orden):
    visitado.add(u)
    orden.append(u)
    for v in grafo[u]:
        if v not in visitado:
            dfs_recursivo(grafo, v, visitado, orden)

orden, visitado = [], set()
dfs_recursivo(grafo, 1, visitado, orden)

print("DFS recursivo:", orden)                      # -> DFS recursivo: [1, 2, 4, 5, 3, 6, 7]
print("DFS iterativo:", dfs_iterativo(grafo, 1))    # -> DFS iterativo: [1, 2, 4, 5, 3, 6, 7]
print("componentes alcanzables desde 1:", len(visitado))  # -> componentes alcanzables desde 1: 7
