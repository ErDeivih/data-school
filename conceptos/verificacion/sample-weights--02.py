import numpy as np

# Cuanto baja la informacion efectiva al alargar las etiquetas: 100 eventos en 300 barras.
rng = np.random.default_rng(0)
n = 300
inicios = np.sort(rng.choice(n, size=100, replace=False))

print("largo  unicidad media  n efectivo")
for largo in (1, 5, 20):
    concurrencia = np.zeros(n)
    for a in inicios:
        concurrencia[a:min(a + largo, n)] += 1
    unicidad = np.array([np.mean(1.0 / concurrencia[a:min(a + largo, n)])
                         for a in inicios if min(a + largo, n) > a])
    print(f"{largo:>5}  {unicidad.mean():>14.3f}  {unicidad.sum():>10.1f}")
# con etiquetas de 20 barras, 100 operaciones valen como 15 independientes
