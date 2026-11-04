# Deteccion de ciclos: BFS por grados de entrada (Kahn) frente a DFS con marcas.
aristas = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]     # DAG: sin ciclos
aristas_ciclicas = [(1, 2), (2, 3), (3, 1), (3, 4)]

def orden_topologico(n, aristas):
    """Kahn: si al final no se han sacado todos, hay ciclo."""
    from collections import deque
    entrantes = {i: 0 for i in range(1, n + 1)}
    salidas = {i: [] for i in range(1, n + 1)}
    for u, v in aristas:
        salidas[u].append(v)
        entrantes[v] += 1
    cola = deque(sorted(i for i in entrantes if entrantes[i] == 0))
    orden = []
    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in salidas[u]:
            entrantes[v] -= 1
            if entrantes[v] == 0:
                cola.append(v)
    return orden if len(orden) == n else None

print("DAG ordenado:", orden_topologico(5, aristas))              # -> DAG ordenado: [1, 2, 3, 4, 5]
print("con ciclo:", orden_topologico(4, aristas_ciclicas))        # -> con ciclo: None
