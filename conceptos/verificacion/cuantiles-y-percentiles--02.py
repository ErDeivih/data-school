import numpy as np

# La misma serie, pero la ultima peticion tarda 1 segundo en vez de 100 ms
latencia = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 1000])
q1, q3 = np.percentile(latencia, [25, 75])

print("media", latencia.mean())                                        # -> 145.0
print("p50  ", np.percentile(latencia, 50))                            # -> 55.0
print("p90  ", round(float(np.percentile(latencia, 90)), 1))           # -> 181.0
print("p95  ", round(float(np.percentile(latencia, 95)), 1))           # -> 590.5

# La valla de Tukey marca como atipico todo lo que supere Q3 + 1,5 * IQR
print("valla", q3 + 1.5 * (q3 - q1))                                   # -> 145.0
