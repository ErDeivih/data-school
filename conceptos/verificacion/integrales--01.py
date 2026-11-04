import numpy as np

# Suma de Riemann: 2000 rectángulos para aproximar el área bajo p(x) = 2*exp(-2x) en [0, 5].
# Con esta rejilla el área sale 0.99996 en vez de 1: la integración numérica siempre tiene error.
x = np.linspace(0, 5, 2001)
y = 2 * np.exp(-2 * x)
area = np.trapezoid(y, x)          # regla de los trapecios sobre una rejilla fina

print("area bajo la densidad ", round(float(area), 5))   # salida: 0.99996
print("P(X > 1) por area    ", round(1 - float(np.trapezoid(y[x <= 1], x[x <= 1])), 6))  # salida: 0.135333
