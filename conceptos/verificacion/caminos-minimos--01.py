import heapq

aristas = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3), (2, 4, 10)]
n = 5

# El grafo es no dirigido: cada arista se guarda en los dos sentidos.
adyacencia = {i: [] for i in range(n)}
for u, v, w in aristas:
    adyacencia[u].append((v, w))
    adyacencia[v].append((u, w))

def dijkstra(adyacencia, origen, n):
    """Distancias minimas desde el origen. Exige pesos no negativos."""
    dist = [float("inf")] * n
    previo = [None] * n
    dist[origen] = 0
    cola = [(0, origen)]                 # (distancia, vertice): el monticulo ordena por distancia
    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue                     # entrada vieja: ya se mejoro por otra ruta
        for v, w in adyacencia[u]:
            if d + w < dist[v]:          # relajacion de la arista (u, v)
                dist[v] = d + w
                previo[v] = u
                heapq.heappush(cola, (dist[v], v))
    return dist, previo

def camino(previo, origen, destino):
    ruta, actual = [], destino
    while actual is not None:
        ruta.append(actual)
        actual = previo[actual]
    ruta.reverse()
    return ruta if ruta and ruta[0] == origen else None

dist, previo = dijkstra(adyacencia, 0, n)
print("distancias desde 0:", dist)          # -> distancias desde 0: [0, 3, 1, 8, 11]
print("camino al 4:", camino(previo, 0, 4)) # -> camino al 4: [0, 2, 4]
print("camino al 3:", camino(previo, 0, 3)) # -> camino al 3: [0, 2, 1, 3]
