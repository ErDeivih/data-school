def floyd_warshall(n, aristas):
    """Todos los pares: programacion dinamica sobre los vertices intermedios."""
    INF = float("inf")
    D = [[INF] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0                      # la distancia de un vertice a si mismo es 0
    for u, v, w in aristas:
        D[u][v] = min(D[u][v], w)        # min() porque puede haber aristas repetidas
    for k in range(n):                   # k: el vertice que se permite como intermedio
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
    return D

D = floyd_warshall(4, [(0, 1, 3), (1, 2, 1), (0, 2, 7), (2, 3, 2)])
print("de 0 a 2:", D[0][2])       # -> de 0 a 2: 4
print("de 0 a 3:", D[0][3])       # -> de 0 a 3: 6
print("de 1 a 3:", D[1][3])       # -> de 1 a 3: 3
print("de 3 a 0:", D[3][0])       # -> de 3 a 0: inf
