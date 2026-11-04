import numpy as np

# Correlacion de Pearson: una parabola perfecta tiene r casi cero.
x = np.linspace(-3, 3, 41)
y = x**2

r = np.corrcoef(x, y)[0, 1]
print("r de x con x^2:", round(r, 3))

# ...y sin embargo la relacion es exacta y determinista.
print("y siempre vale x^2:", bool(np.allclose(y, x**2)))
