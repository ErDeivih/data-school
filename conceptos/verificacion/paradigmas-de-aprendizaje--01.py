import numpy as np

# Doce clientes: x = horas de uso al mes, y = gasto mensual
x = np.array([1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
y = np.array([8.0, 11, 15, 14, 19, 22, 21, 26, 30, 29, 34, 37])

# Supervisado: conocemos y y queremos predecirla con una recta (minimos cuadrados)
pendiente, intercepto = np.polyfit(x, y, 1)
print("recta: gasto = %.2f + %.2f * horas" % (intercepto, pendiente))
# -> recta: gasto = 5.71 + 2.53 * horas
print("RMSE en la muestra %.2f" % np.sqrt(np.mean((y - (pendiente * x + intercepto)) ** 2)))
# -> RMSE en la muestra 1.33

# No supervisado: dos grupos con K-means sobre los pares (x, y), sin etiquetas
datos = np.column_stack([x, y])
centros = np.array([datos[0], datos[-1]], dtype=float)   # arranque: el primero y el ultimo
for _ in range(20):                       # iterar hasta que los grupos se estabilicen
    distancias = np.sqrt(((datos[:, None, :] - centros[None, :, :]) ** 2).sum(axis=2))
    etiquetas = distancias.argmin(axis=1)
    centros = np.array([datos[etiquetas == k].mean(axis=0) for k in (0, 1)])
print("tamano de los grupos", np.bincount(etiquetas, minlength=2).tolist())
# -> tamano de los grupos [7, 5]
for cx, cy in centros:
    print("centroide: %.1f horas, %.1f euros" % (cx, cy))
# -> centroide: 4.0 horas, 15.7 euros
# -> centroide: 10.0 horas, 31.2 euros
