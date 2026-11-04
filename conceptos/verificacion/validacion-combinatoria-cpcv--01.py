import numpy as np
from itertools import combinations

n_grupos, k, por_grupo = 6, 2, 100
combos = list(combinations(range(n_grupos), k))
print(f"N={n_grupos}, k={k}: {len(combos)} caminos de prueba")     # -> 15
print(f"cada camino prueba {k * por_grupo} de {n_grupos * por_grupo} observaciones")  # -> 200

# Purga: cada bloque de prueba invalida las etiquetas vecinas que solapan con el.
largo = 10
purgadas = []
for combo in combos:
    prueba = np.zeros(n_grupos * por_grupo, dtype=bool)
    bandas = np.zeros(n_grupos * por_grupo, dtype=bool)
    for g in combo:
        prueba[g * por_grupo:(g + 1) * por_grupo] = True
        bandas[max(0, g * por_grupo - largo + 1):(g + 1) * por_grupo + largo - 1] = True
    purgadas.append(int((bandas & ~prueba).sum()))
print(f"purgadas por camino: min {min(purgadas)}  max {max(purgadas)}  "
      f"media {np.mean(purgadas):.1f}")        # -> min 9  max 36  media 24.0
