import numpy as np

# Correlacion cruzada 2D a mano: es lo que hacen las librerias (sin girar el filtro).
imagen = np.array([[0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 1, 1, 1, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0]], dtype=float)
# Filtro que detecta un borde vertical: negativo a la izquierda, positivo a la derecha.
filtro = np.array([[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]], dtype=float)

salida = np.zeros((3, 3))          # float64 por defecto: con dtype=int cada suma se truncaria
for i in range(3):                 # range(3) porque 5 - 3 + 1 = 3 posiciones validas
    for j in range(3):
        # imagen[i:i+3, j:j+3] es una VISTA, no una copia: no gasta memoria y escribir en
        # ella modificaria la imagen original. El * es elemento a elemento, no matricial.
        salida[i, j] = (imagen[i:i+3, j:j+3] * filtro).sum()

# astype devuelve una COPIA convertida a entero y tolist() la pasa a listas de Python: sin
# los dos se imprimiria un array de numpy, con un formato que cambia segun la version.
print(salida.astype(int).tolist())   # -> [[2, 0, -2], [3, 0, -3], [2, 0, -2]]
