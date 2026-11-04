from itertools import combinations

# Dos mayorias cualesquiera se cruzan: eso es toda la seguridad del consenso.
for n in (3, 5, 7):
    mayoria = n // 2 + 1
    # combinations devuelve tuplas de tamano "mayoria": todos los grupos que podrian decidir.
    conjuntos = list(combinations(range(n), mayoria))
    # set(a) & set(b) es la interseccion; len() cuenta cuantos nodos comparten. El min sobre
    # todas las parejas da el peor caso, que es el que importa para la seguridad.
    cruce_minimo = min(len(set(a) & set(b)) for a in conjuntos for b in conjuntos)
    print(f"N={n}: {len(conjuntos)} mayorias de tamano {mayoria},"
          f" interseccion minima entre dos = {cruce_minimo}")
