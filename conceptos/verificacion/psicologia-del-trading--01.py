# Probabilidad de al menos una racha de k perdidas en n operaciones.
def prob_racha(n, k, p_perder):
    estados = {(0, False): 1.0}          # (racha actual, ya ha aparecido una racha de k)
    for _ in range(n):
        nuevo = {}
        for (racha, hubo), prob in estados.items():
            for pierde, p in ((True, p_perder), (False, 1 - p_perder)):
                nr = racha + 1 if pierde else 0
                clave = (min(nr, k), hubo or nr >= k)
                nuevo[clave] = nuevo.get(clave, 0.0) + prob * p
        estados = nuevo
    return sum(pr for (r, h), pr in estados.items() if h)

for k in (5, 7, 10, 12):
    print(f"racha de {k:>2} perdidas en 200 ops: {prob_racha(200, k, 0.55):>6.1%}   "
          f"en 1000 ops: {prob_racha(1000, k, 0.55):>6.1%}")
