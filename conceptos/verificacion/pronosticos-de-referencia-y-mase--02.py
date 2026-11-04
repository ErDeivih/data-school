import numpy as np

# Una serie sencilla para ver de donde sale el 1 del MASE.
y = np.array([3.0, 5.0, 4.0, 6.0, 8.0, 7.0, 9.0])
escala = np.abs(y[1:] - y[:-1]).mean()          # lo que falla el ingenuo en muestra
error = y[1:] - y[:-1]                          # el error del ingenuo, uno a uno
print("escala", round(escala, 4))               # -> escala 1.6667
print("MASE del ingenuo", round(np.abs(error).mean() / escala, 4))
# -> MASE del ingenuo 1.0

# El sMAPE no es simetrico: pasarse y quedarse corto no cuestan lo mismo.
real, alto, bajo = 30.0, 45.0, 15.0
print("sMAPE si me paso:", round(2 * abs(real - alto) / (abs(real) + abs(alto)), 4))
# -> sMAPE si me paso: 0.4
print("sMAPE si me quedo corto:", round(2 * abs(real - bajo) / (abs(real) + abs(bajo)), 4))
# -> sMAPE si me quedo corto: 0.6667

# El MAPE no existe si un valor real es cero; el MASE si.
real = np.array([0.0, 4.0, 6.0, 5.0, 7.0])      # un mes sin ventas
pred = np.array([3.0, 0.0, 4.0, 6.0, 5.0])      # el pronostico ingenuo: el mes anterior
with np.errstate(divide="ignore"):              # dividir entre cero da inf, no una excepcion
    print("MAPE con un cero:", np.abs((real - pred) / real).mean())   # -> inf
print("denominador del MASE:", round(np.abs(real[1:] - real[:-1]).mean(), 3))
# -> denominador del MASE: 2.25
