import numpy as np

rng = np.random.default_rng(7)
rondas = 20_000

def empate(timeouts):
    """Hay empate si mas de un nodo expira en el mismo instante minimo."""
    # timeouts.min() da el tiempo mas corto de la ronda; la comparacion produce un array de
    # booleanos y .sum() cuenta cuantos son True. Con mas de uno, hay empate en el minimo.
    return int((timeouts == timeouts.min()).sum()) > 1

# Temporizadores sorteados por cada nodo entre 150 y 300 ms
# size=(rondas, 5) crea una matriz de 20.000 rondas por 5 nodos; integers excluye el 301.
aleatorios = rng.integers(150, 301, size=(rondas, 5))
# Temporizadores iguales para todos: el error de configuracion clasico
iguales = np.full((rondas, 5), 200)

# map aplica empate() a cada fila de la matriz; sum() cuenta cuantas rondas empataron.
print(f"timeouts aleatorios: {100 * sum(map(empate, aleatorios)) / rondas:.1f} % de rondas con empate")   # -> 1.7 %
print(f"timeouts iguales:    {100 * sum(map(empate, iguales)) / rondas:.1f} % de rondas con empate")      # -> 100.0 %
