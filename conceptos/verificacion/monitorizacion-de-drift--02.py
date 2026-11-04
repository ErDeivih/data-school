import numpy as np

# Deriva de concepto: las entradas son las mismas, la regla que genera y ha cambiado.
rng = np.random.default_rng(0)
x = rng.normal(0.0, 1.0, size=2000)
y_train = 2.0 * x + rng.normal(0.0, 1.0, size=2000)
y_prod = -2.0 * x + rng.normal(0.0, 1.0, size=2000)

pendiente = float(np.polyfit(x, y_train, 1)[0])        # lo que aprendio el modelo
mse_train = float(((y_train - pendiente * x) ** 2).mean())
mse_prod = float(((y_prod - pendiente * x) ** 2).mean())

print("corr en entrenamiento:", round(float(np.corrcoef(x, y_train)[0, 1]), 3))  # -> 0.894
print("corr en produccion:   ", round(float(np.corrcoef(x, y_prod)[0, 1]), 3))   # -> -0.897
print("MSE en entrenamiento: ", round(mse_train, 2))                             # -> 0.99
print("MSE en produccion:    ", round(mse_prod, 2))                              # -> 16.93
