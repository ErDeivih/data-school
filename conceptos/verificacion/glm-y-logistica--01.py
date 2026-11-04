import numpy as np
from sklearn.linear_model import LogisticRegression

# Horas de estudio (x) y resultado del examen (1 aprueba, 0 suspende).
x = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0]).reshape(-1, 1)
y = np.array([0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1])

# reshape(-1, 1) convierte los 12 numeros en una matriz de 12 filas y 1 columna:
# sklearn espera una tabla de variables, no una lista plana.
modelo = LogisticRegression().fit(x, y)
b0, b1 = modelo.intercept_[0], modelo.coef_[0, 0]

print(f"b0 {b0:.3f}  b1 {b1:.3f}")
print(f"odds ratio por hora extra {np.exp(b1):.3f}")
for horas in (4.0, 6.0):
    p = 1 / (1 + np.exp(-(b0 + b1 * horas)))          # funcion logistica
    # predict_proba devuelve dos columnas (clase 0 y clase 1): el [0, 1] toma la segunda.
    print(f"h={horas:.1f}  sigmoide {p:.3f}  sklearn {modelo.predict_proba([[horas]])[0, 1]:.3f}")
# -> b0 -4.774  b1 1.271
# -> odds ratio por hora extra 3.563
# -> h=4.0  sigmoide 0.576  sklearn 0.576
# -> h=6.0  sigmoide 0.945  sklearn 0.945
