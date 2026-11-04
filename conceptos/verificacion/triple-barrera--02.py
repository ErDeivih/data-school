import numpy as np

# Dos caminos con el mismo destino y etiquetas opuestas: la etiqueta depende del recorrido.
camino_a = np.array([100.0, 101.0, 102.5, 103.2, 104.0])
camino_b = np.array([100.0, 99.0, 97.5, 101.0, 104.0])
arriba, abajo = 100 * 1.02, 100 * 0.98

def primera_barrera(camino, arriba, abajo):
    for i in range(1, camino.size):
        if camino[i] >= arriba:
            return i, 1
        if camino[i] <= abajo:
            return i, -1
    return camino.size - 1, 0

# Los dos caminos acaban en 104 (+4 %), pero la primera barrera es distinta en cada uno.
for nombre, c in (("A", camino_a), ("B", camino_b)):
    i, etq = primera_barrera(c, arriba, abajo)
    print(f"camino {nombre}: retorno final {c[-1]/c[0]-1:+.1%}  "
          f"primera barrera en t={i}  etiqueta {etq:+d}")
