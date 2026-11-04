import numpy as np

serie = np.array([10.0, 12.0, 11.0, 13.0])

def sse_ses(alfa, y):
    """Suma de errores al cuadrado a un paso de un suavizado exponencial simple."""
    pred = y[0]                      # el primer pronostico es el primer dato
    sse = 0.0
    for t in range(1, y.size):
        sse += (y[t] - pred) ** 2
        pred = alfa * y[t] + (1 - alfa) * pred
    return sse

for a in (0.25, 0.5, 0.9):
    print("alfa %.2f  SSE %.4f" % (a, sse_ses(a, serie)))
# -> alfa 0.25 SSE 9.8906   alfa 0.50 SSE 8.0000   alfa 0.90 SSE 8.3264
mejor = max(np.arange(0.05, 1.0, 0.05), key=lambda a: -sse_ses(a, serie))
print("mejor alfa %.2f  SSE %.4f" % (mejor, sse_ses(mejor, serie)))   # -> 0.65 y 7.6810
