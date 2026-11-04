import random
import zlib

# Las mismas 20 ciudades con las mismas frecuencias, en dos ordenes distintos
ciudades = [f"ciudad_{i % 20:02d}" for i in range(20_000)]
mezcladas = ciudades[:]
random.Random(0).shuffle(mezcladas)          # semilla fija: el resultado es reproducible

en_ciclo = ",".join(ciudades).encode()       # ciudad_00, ciudad_01, ... y vuelta a empezar
al_azar = ",".join(mezcladas).encode()       # mismas frecuencias, orden aleatorio

print("bytes crudos iguales:", len(en_ciclo) == len(al_azar))    # -> bytes crudos iguales: True
print("comprime mejor el orden agrupado:", len(zlib.compress(en_ciclo, 6)) < len(zlib.compress(al_azar, 6)))  # -> comprime mejor el orden agrupado: True
print("zlib agrupado baja de 100 kB:", len(zlib.compress(en_ciclo, 6)) < 100_000)  # -> zlib agrupado baja de 100 kB: True
