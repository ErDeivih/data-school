import numpy as np

rng = np.random.default_rng(0)
x_grid = np.linspace(0, 3, 200)

# k vecinos mas cercanos a 1.0 sobre una rejilla densa: el diseno es fijo,
# asi que los vecinos no cambian entre muestras; lo que cambia es el ruido.
distancias = np.abs(x_grid - 1.0)
vecinos = np.argsort(distancias)

print("  k   error   sesgo^2   varianza")
for k in (1, 5, 20, 60, 200):
    predicciones = []
    for _ in range(400):
        y_ruidoso = 2.0 + 0.5 * x_grid + rng.normal(0, 0.3, size=x_grid.size)
        predicciones.append(y_ruidoso[vecinos[:k]].mean())
    predicciones = np.array(predicciones)
    verdadero = 2.0 + 0.5 * 1.0
    error = ((predicciones - verdadero) ** 2).mean()
    print(f"{k:>3}  {error:.4f}  {(predicciones.mean() - verdadero) ** 2:.4f}   {predicciones.var():.4f}")
