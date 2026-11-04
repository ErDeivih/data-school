# Coste real: matriz cuadratica frente a lista lineal, con un grafo disperso.
import random

def memoria_estimada(n, m):
    """Celdas de la matriz frente a entradas de la lista, en unidades de referencia."""
    return n * n, n + 2 * m      # la lista no dirigida guarda cada arista dos veces

for n in (100, 1_000, 10_000):
    m = 5 * n                    # grafo disperso: 5 vecinos por vertice de media
    celdas, entradas = memoria_estimada(n, m)
    print(f"n={n:>6}  m={m:>6}  matriz={celdas:>12}  lista={entradas:>8}  factor={celdas / entradas:.0f}")
