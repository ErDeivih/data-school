import numpy as np

# Acumular gradientes: la suma dividida entre los pasos da el gradiente del lote grande.
micro, acumulacion = 8, 4
print("lote efectivo:", micro * acumulacion)          # -> 32

deltas = [np.array([1.0, 3.0]), np.array([3.0, 5.0]),
          np.array([2.0, 2.0]), np.array([2.0, 2.0])]
# sum() arranca en el entero 0 y va sumando arrays uno a uno: el resultado es un array nuevo
medio = sum(deltas) / len(deltas)
print("gradiente medio:", medio.round(2).tolist())     # -> [2.0, 3.0]
print("suma sin dividir:", sum(deltas).round(2).tolist())  # -> [8.0, 12.0]
