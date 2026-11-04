import numpy as np

# La maldicion de la dimensionalidad, medida: en muchas dimensiones
# el vecino mas cercano y el mas lejano estan casi a la misma distancia.
rng = np.random.default_rng(0)
print("dim  dist. al vecino mas cercano  al mas lejano  cociente")
for d in (2, 5, 20, 100, 500):
    X = rng.uniform(size=(1000, d))     # 1000 puntos en una caja de lado 1
    q = rng.uniform(size=d)             # el punto nuevo, tambien al azar
    # X - q resta el vector a las 1000 filas; axis=1 suma las d coordenadas de
    # cada punto, que es la distancia euclidea al cuadrado antes de la raiz.
    dist = np.sqrt(((X - q) ** 2).sum(axis=1))
    print(f"{d:>4}  {dist.min():>28.3f}  {dist.max():>12.3f}  {dist.min() / dist.max():>8.3f}")
# -> dim  dist. al vecino mas cercano  al mas lejano  cociente
# ->    2                         0.010         1.334     0.007
# ->    5                         0.144         1.633     0.088
# ->   20                         1.047         2.267     0.462
# ->  100                         3.013         4.899     0.615
# ->  500                         8.198         9.755     0.840
