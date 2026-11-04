def mochila_01(pesos, valores, capacidad):
    """Tabulacion de la mochila 0/1. Devuelve (valor optimo, objetos elegidos)."""
    n = len(pesos)
    # F[i][c] = mejor valor usando los i primeros objetos con capacidad c
    F = [[0] * (capacidad + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for c in range(capacidad + 1):
            F[i][c] = F[i - 1][c]                       # opcion: no coger el objeto i
            if pesos[i - 1] <= c:
                con = valores[i - 1] + F[i - 1][c - pesos[i - 1]]
                if con > F[i][c]:
                    F[i][c] = con                       # opcion: cogerlo
    # Reconstruccion hacia atras: si el valor cambio al anadir el objeto, se cogio
    elegidos, c = [], capacidad
    for i in range(n, 0, -1):
        if F[i][c] != F[i - 1][c]:
            elegidos.append(i - 1)
            c -= pesos[i - 1]
    return F[n][capacidad], sorted(elegidos)

pesos = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
valor, elegidos = mochila_01(pesos, valores, 5)
print("valor optimo:", valor)                      # -> valor optimo: 7
print("objetos elegidos:", elegidos)               # -> objetos elegidos: [0, 1]
print("estados evaluados:", len(pesos) * 6)        # -> estados evaluados: 24
