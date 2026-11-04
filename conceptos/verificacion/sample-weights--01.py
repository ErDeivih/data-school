import numpy as np

t0 = np.array([0, 2, 6, 8])
t1 = np.array([5, 7, 9, 12])
n_barras = 12

# Concurrencia: cuantas etiquetas estan vivas en cada barra.
concurrencia = np.zeros(n_barras, dtype=int)
for a, b in zip(t0, t1):
    concurrencia[a:b] += 1
print("concurrencia por barra:", concurrencia.tolist())
# -> [1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1]

# Unicidad: media de 1/concurrencia a lo largo de la vida de cada etiqueta.
unicidad = np.array([np.mean(1.0 / concurrencia[a:b]) for a, b in zip(t0, t1)])
print("unicidad:", np.round(unicidad, 3).tolist())        # -> [0.7, 0.6, 0.667, 0.875]

# Se normaliza para que la suma de pesos siga siendo el numero de observaciones.
pesos = unicidad / unicidad.sum() * unicidad.size
print("pesos normalizados:", np.round(pesos, 3).tolist())  # -> [0.985, 0.845, 0.938, 1.232]
