import numpy as np

latencia = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# NumPy interpola entre los dos valores ordenados que rodean la posicion buscada
print("p50        ", np.percentile(latencia, 50))                        # -> 55.0
print("p90        ", np.percentile(latencia, 90))                        # -> 91.0
print("p95        ", round(float(np.percentile(latencia, 95)), 1))       # -> 95.5

# El rango mas cercano no interpola: devuelve un valor observado
print("p95 nearest", np.percentile(latencia, 95, method="nearest"))      # -> 100

# Los cuartiles son los percentiles 25 y 75; su diferencia es el IQR
q1, q3 = np.percentile(latencia, [25, 75])
print("IQR        ", q3 - q1)                                           # -> 45.0
