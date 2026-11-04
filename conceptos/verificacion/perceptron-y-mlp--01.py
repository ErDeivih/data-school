import numpy as np
from sklearn.datasets import make_circles
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Clase 0 dentro del circulo, clase 1 en el anillo: ninguna recta las separa
X, y = make_circles(n_samples=400, factor=0.4, noise=0.08, random_state=0)
# factor=0.4 es el radio del circulo interior; noise añade ruido a las coordenadas
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

lineal = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
# score() devuelve la exactitud (aciertos partido por filas), no la perdida
print("regresion logistica:", round(float(lineal.score(X_te, y_te)), 3))    # -> 0.425

for capas in ((2,), (8,)):
    red = MLPClassifier(hidden_layer_sizes=capas, max_iter=3000,
                        early_stopping=False, random_state=0).fit(X_tr, y_tr)
    # coefs_ es una lista con la matriz de cada capa e intercepts_ la lista de sesgos
    n_par = red.coefs_[0].size + red.intercepts_[0].size + red.coefs_[1].size + 1
    # capas es una tupla: (8,) es una capa de 8 neuronas y (8, 4) serian dos capas
    print(f"una capa de {capas[0]} neuronas:", round(float(red.score(X_te, y_te)), 3),
          " parametros:", n_par)
# -> una capa de 2 neuronas: 0.775  parametros: 9
# -> una capa de 8 neuronas: 1.0  parametros: 33

# XOR: el caso minimo que una sola neurona nunca resuelve
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])
red = MLPClassifier(hidden_layer_sizes=(8,), max_iter=5000, early_stopping=False,
                    random_state=1).fit(X_xor, y_xor)
print("XOR con capa oculta:", red.predict(X_xor), " (esperado [0 1 1 0])")   # -> [0 1 1 0]
