import numpy as np

# Cuantos parametros gasta cada celda con entrada 10 y estado oculto 20.
d, m = 10, 20                                  # d entradas por paso, m unidades de estado
rnn = d * m + m * m + m                        # una matriz de entrada, una recurrente, un sesgo
lstm = 4 * (d * m + m * m) + 4 * m             # 4 puertas
gru = 3 * (d * m + m * m) + 3 * m              # 3 puertas
print("RNN :", rnn)                 # -> 620
print("LSTM:", lstm)                # -> 2480
print("GRU :", gru)                 # -> 1860
print("GRU/LSTM:", round(gru / lstm, 3))   # -> 0.75

# Una celda RNN minima paso a paso: h_t = tanh(x_t Wx + h_(t-1) Wh + b).
rng = np.random.default_rng(0)                 # semilla fija: los mismos numeros siempre
Wx = rng.normal(0, 0.1, (d, m))                # (entradas, unidades): x[t] @ Wx -> (m,)
Wh = rng.normal(0, 0.1, (m, m))                # (unidades, unidades): h @ Wh -> (m,)
b = np.zeros(m)
x = rng.normal(0, 1, (5, d))                   # 5 pasos de tiempo, d entradas por paso

h = np.zeros(m)                                # estado inicial: un vector plano de ceros
for t in range(5):                             # la MISMA celda cinco veces: pesos atados
    h = np.tanh(x[t] @ Wx + h @ Wh + b)

# El estado final es todo lo que la red recuerda de los 5 pasos.
print("norma del estado:", round(float(np.linalg.norm(h)), 4))   # -> 1.3989
