from scipy import integrate
import numpy as np

# La integral de una densidad es la probabilidad, y E[X] se calcula pesando cada x por su densidad.
p = lambda x: 2 * np.exp(-2 * x)

esperanza, error = integrate.quad(lambda x: x * p(x), 0, np.inf)
prob_mayor_1, _ = integrate.quad(p, 1, np.inf)

print("E[X]      ", round(esperanza, 6), "+-", round(error, 2))   # salida: 0.5 +- 0.0
print("P(X > 1)  ", round(prob_mayor_1, 6))                        # salida: 0.135335
print("e elevado a -2:", round(np.exp(-2), 6))                     # salida: 0.135335
