import numpy as np
from scipy import stats

equipo_a = np.array([48, 49, 50, 51, 52], dtype=float)
equipo_b = np.array([10, 30, 50, 70, 90], dtype=float)

# La misma media en los dos equipos: sin dispersion serian indistinguibles
print("media   ", equipo_a.mean(), equipo_b.mean())                     # -> 50.0 50.0
print("rango   ", equipo_a.max() - equipo_a.min(),
      equipo_b.max() - equipo_b.min())                                  # -> 4.0 80.0
print("sd      ", round(float(equipo_a.std(ddof=1)), 2),
      round(float(equipo_b.std(ddof=1)), 2))                            # -> 1.58 31.62
print("varianza", equipo_a.var(ddof=1), equipo_b.var(ddof=1))           # -> 2.5 1000.0
print("CV %    ", round(100 * float(equipo_a.std(ddof=1) / equipo_a.mean()), 1),
      round(100 * float(equipo_b.std(ddof=1) / equipo_b.mean()), 1))    # -> 3.2 63.2
print("MAD     ", stats.median_abs_deviation(equipo_a),
      stats.median_abs_deviation(equipo_b))                             # -> 1.0 20.0
