import numpy as np

# Los cinco tramos de la tabla del ejemplo: el clasico exceso de confianza arriba
confianza = np.array([0.12, 0.31, 0.52, 0.71, 0.88])
casos = np.array([300, 250, 200, 150, 100])
observada = np.array([0.10, 0.28, 0.55, 0.62, 0.74])

# ECE: media de los desvios ponderada por el tamano de cada tramo
# casos / casos.sum() divide elemento a elemento: cada tramo se lleva su peso y los cinco
# pesos suman 1. No hace falta ningun bucle.
desvios = np.abs(observada - confianza)
ece = float((casos / casos.sum() * desvios).sum())
# np.round devuelve otro array; .tolist() lo convierte en lista de Python para que se
# imprima como [0.02, 0.03, ...] y no como array([0.02, 0.03, ...]).
print("desvios por tramo", np.round(desvios, 2).tolist())  # -> [0.02, 0.03, 0.03, 0.09, 0.14]
print(f"ECE {ece:.4f}")                                    # -> 0.0470
