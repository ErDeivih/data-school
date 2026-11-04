import numpy as np

# Retrasos de llegada de una semana, en minutos (semilla fija para que sea reproducible)
azar = np.random.default_rng(7)
retrasos = azar.gamma(shape=2.0, scale=1.5, size=20000)

print(f"p50 {np.percentile(retrasos, 50):.2f} min")     # -> p50 2.51 min
print(f"p90 {np.percentile(retrasos, 90):.2f} min")     # -> p90 5.82 min
print(f"p99 {np.percentile(retrasos, 99):.2f} min")     # -> p99 9.83 min
# Con R = 10 entra el 99 % de los eventos; con R = 3, la mitad se queda fuera.
