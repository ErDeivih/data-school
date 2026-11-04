def bellman_ford(n, aristas, origen):
    """Admite pesos negativos. Devuelve None si hay un ciclo de peso negativo alcanzable."""
    dist = [float("inf")] * n
    dist[origen] = 0
    for _ in range(n - 1):               # n-1 pasadas bastan para cualquier camino simple
        for u, v, w in aristas:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in aristas:              # una pasada mas: si algo mejora, hay ciclo negativo
        if dist[u] + w < dist[v]:
            return None
    return dist

# Camino barato que pasa por dos aristas negativas seguidas
sin_ciclo = [(0, 1, 3), (0, 2, 1), (2, 3, 2), (3, 1, -4), (1, 4, 5), (3, 4, 7)]
print("pesos negativos:", bellman_ford(5, sin_ciclo, 0))   # -> pesos negativos: [0, -1, 1, 3, 4]

# Un ciclo cuyo peso total es negativo: no existe el camino minimo
ciclo_negativo = [(0, 1, 1), (1, 2, -3), (2, 1, 1)]
print("ciclo negativo:", bellman_ford(3, ciclo_negativo, 0))  # -> ciclo negativo: None
