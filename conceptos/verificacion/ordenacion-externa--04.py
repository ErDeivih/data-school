import heapq
import numpy as np

# Seleccion por reemplazo: el monticulo no se vacia del todo, asi que las vueltas salen
# mas largas que M. En datos al azar la longitud media tiende a 2M.
azar = np.random.default_rng(7)
M = 500                                        # registros que caben en memoria
datos = list(azar.integers(0, 10 ** 9, size=20000).tolist())   # el fichero de entrada

i, largos, monton = 0, [], []
while i < len(datos) or monton:
    while len(monton) < M and i < len(datos):
        heapq.heappush(monton, datos[i]); i += 1
    congelados, larga = [], 0
    while monton:
        x = heapq.heappop(monton)              # el menor candidato sale ya a su vuelta
        larga += 1
        if i < len(datos):
            nuevo = datos[i]; i += 1
            if nuevo >= x:                     # encaja detras de x: sigue en esta vuelta
                heapq.heappush(monton, nuevo)
            else:
                congelados.append(nuevo)       # ya no: espera a la vuelta siguiente
    largos.append(larga)
    monton = congelados
    heapq.heapify(monton)

print("vueltas:", len(largos))                          # -> vueltas: 21
print("longitud media:", round(sum(largos) / len(largos)))   # -> longitud media: 952
print("vueltas de M en M serian:", -(-len(datos) // M))      # -> vueltas de M en M serian: 40
