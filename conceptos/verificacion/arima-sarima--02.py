import numpy as np

rng = np.random.default_rng(2)
n = 300
phi = 0.6
x = np.zeros(n)
for t in range(1, n):                       # diferencias: un AR(1) estacionario
    x[t] = phi * x[t - 1] + rng.normal(0, 1)
y = 100 + np.cumsum(x)                      # la serie: un ARIMA(1,1,0)

dy = np.diff(y)
X = np.column_stack([np.ones(dy.size - 1), dy[:-1]])   # constante y retardo 1
b, *_ = np.linalg.lstsq(X, dy[1:], rcond=None)
print("phi estimado %.3f  (el simulado era %.1f)" % (b[1], phi))   # -> 0.560

# Pronostico: se predice la diferencia y se vuelve a integrar sobre el ultimo nivel
pred = dy[-1]
camino = [y[-1]]
for h in range(3):
    pred = b[0] + b[1] * pred
    camino.append(camino[-1] + pred)
print("ultimo dato %.2f" % y[-1])                        # -> 61.15
print("pronostico 1 a 3 pasos", np.round(camino[1:], 2))  # -> [59.9  59.14 58.65]
print("efecto de un shock de -2 en un MA(1) con theta=0.6: %.2f" % (0.6 * -2))  # -> -1.20
