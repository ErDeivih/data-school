def bloques(filas, por_bloque=100):
    return -(-filas // por_bloque)          # division hacia arriba

def miles(x):
    return f"{x:,}".replace(",", ".")       # millares a la espanola

def ordenar_externo(b, M, k):
    """Bloques movidos al ordenar b bloques con M en memoria y fusiones de k vias."""
    vueltas, rondas = -(-b // M), 0
    while vueltas > 1:
        vueltas = -(-vueltas // k)
        rondas += 1
    return 2 * b * (1 + rondas)

n_A, n_B = 10_000_000, 200_000              # tabla de hechos y tabla de dimension
b_A, b_B = bloques(n_A), bloques(n_B)
print("bloques de A y B:", miles(b_A), miles(b_B))            # -> bloques de A y B: 100.000 2.000
print("bucle anidado por bloques:", miles(b_B + b_B * b_A))
# -> bucle anidado por bloques: 200.002.000
print("hash en memoria:", miles(b_A + b_B))                   # -> hash en memoria: 102.000
print("Grace hash a disco:", miles(3 * (b_A + b_B)))          # -> Grace hash a disco: 306.000
print("sort-merge ya ordenado:", miles(b_A + b_B))            # -> sort-merge ya ordenado: 102.000
ordenar = ordenar_externo(b_A, 5000, 10) + ordenar_externo(b_B, 5000, 10)
print("ordenar las dos antes:", miles(ordenar))               # -> ordenar las dos antes: 604.000
print("sort-merge completo:", miles(ordenar + b_A + b_B))     # -> sort-merge completo: 706.000
