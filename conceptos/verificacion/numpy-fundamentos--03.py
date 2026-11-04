import time

import numpy as np

v = np.arange(500_000, dtype=np.float64)
lista = v.tolist()

t0 = time.perf_counter()
a1 = 0.0
for x in lista:             # la forma mas rapida de recorrer en Python: lista de floats
    a1 += x
t1 = time.perf_counter()
a2 = 0.0
for i in range(v.size):     # indexar el array en cada vuelta es peor: crea un escalar nuevo
    a2 += v[i]
t2 = time.perf_counter()
total = float(v.sum())      # un unico bucle en C sobre memoria contigua
t3 = time.perf_counter()

print(f"bucle sobre lista  {1000 * (t1 - t0):.0f} ms")   # los tiempos dependen de la maquina
print(f"bucle indexando    {1000 * (t2 - t1):.0f} ms")
print(f"numpy              {1000 * (t3 - t2):.2f} ms")
print("mismo resultado:", abs(a1 - total) < 1e-6 and abs(a2 - total) < 1e-6)   # -> mismo resultado: True

# Los tipos tienen ancho fijo: si te pasas del rango no hay error, hay vuelta a empezar
c = np.array([120], dtype=np.int8)
print((c + np.int8(10)).tolist())   # -> [-126]
