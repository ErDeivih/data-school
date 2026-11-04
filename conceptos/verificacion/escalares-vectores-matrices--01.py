import numpy as np

# Dataset de 4 personas: edad, altura en cm y peso en kg (una fila por persona)
datos = np.array([[34, 171,  68],
                  [51, 165,  71],
                  [28, 180,  84],
                  [45, 158,  57]])

print("forma (filas, columnas):", datos.shape)       # -> (4, 3)
print("elemento fila 2, col 3:", datos[1, 2])        # -> 71
print("una fila (persona 1):", datos[0])             # -> [ 34 171  68]
print("una columna (peso):", datos[:, 2])            # -> [68 71 84 57]
print("numero de valores:", datos.size)              # -> 12
