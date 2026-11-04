import numpy as np

ventas = np.array([50.0, 62, 58, 70, 55, 68, 63, 76, 60, 74, 69, 83])

def hw(y, m, alfa, beta, gamma):
    """Holt-Winters aditivo: nivel, tendencia y estacionalidad de m periodos."""
    n = y.size
    nivel = y[:m].mean()
    tend = (y[m:2 * m].mean() - nivel) / m
    est = list(y[:m] - nivel) * (n // m + 2)        # un ciclo inicial de estacionalidad
    sse = 0.0
    for t in range(n):
        sse += (y[t] - (nivel + tend + est[t])) ** 2
        nuevo_nivel = alfa * (y[t] - est[t]) + (1 - alfa) * (nivel + tend)
        est[t + m] = gamma * (y[t] - nivel - tend) + (1 - gamma) * est[t]
        tend = beta * (nuevo_nivel - nivel) + (1 - beta) * tend
        nivel = nuevo_nivel
    return sse, nivel, tend, est

mejor = None
for alfa in np.arange(0.1, 0.95, 0.1):
    for beta in np.arange(0.05, 0.65, 0.1):
        for gamma in np.arange(0.1, 0.95, 0.1):
            s, *_ = hw(ventas, 4, alfa, beta, gamma)
            if mejor is None or s < mejor[0]:
                mejor = (s, round(alfa, 2), round(beta, 2), round(gamma, 2))
sse, nivel, tend, est = hw(ventas, 4, mejor[1], mejor[2], mejor[3])
print("rejilla: alfa %.2f  beta %.2f  gamma %.2f  SSE %.1f" % (mejor[1], mejor[2], mejor[3], mejor[0]))
# -> alfa 0.50  beta 0.05  gamma 0.30  SSE 36.8
print("nivel final %.2f  tendencia final %.2f" % (nivel, tend))     # -> 73.80 y 1.30
print("pronostico 4 trimestres", np.round([nivel + h * tend + est[ventas.size + h - 1] for h in range(1, 5)], 1))
# -> [65.9 78.8 74.5 88.1]
print("RMSE dentro de la muestra %.2f" % np.sqrt(sse / ventas.size))  # -> 1.75
