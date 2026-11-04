import numpy as np
from sklearn.preprocessing import StandardScaler

# Escalar antes de dividir contamina: la media y la desviacion incluyen la prueba.
datos = np.array([[2.0], [4.0], [6.0], [8.0], [998.0]])
entrenamiento, prueba = datos[:4], datos[4:]

mal = StandardScaler().fit(datos)            # vio la fila de prueba
bien = StandardScaler().fit(entrenamiento)   # solo el entrenamiento

print(f"media usada con fuga {mal.mean_[0]:.0f}")    # -> 204
print(f"media usada sin fuga {bien.mean_[0]:.0f}")   # -> 5
print(f"prueba con fuga {mal.transform(prueba)[0, 0]:.2f}")    # -> 2.00
print(f"prueba sin fuga {bien.transform(prueba)[0, 0]:.2f}")   # -> 444.08
