def distancia_edicion(a, b):
    """Distancia de Levenshtein por tabulacion: insertar, borrar o sustituir."""
    n, m = len(a), len(b)
    # D[i][j] = coste de convertir a[:i] en b[:j]
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i                  # borrar todo lo que sobra
    for j in range(m + 1):
        D[0][j] = j                  # insertar todo lo que falta
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            coste = 0 if a[i - 1] == b[j - 1] else 1
            D[i][j] = min(D[i - 1][j] + 1,        # borrar
                          D[i][j - 1] + 1,        # insertar
                          D[i - 1][j - 1] + coste)  # sustituir o dejar igual
    return D[n][m]

print("casa -> calle:", distancia_edicion("casa", "calle"))     # -> casa -> calle: 3
print("iguales:", distancia_edicion("datos", "datos"))          # -> iguales: 0
print("estados:", (4 + 1) * (5 + 1))                            # -> estados: 30
