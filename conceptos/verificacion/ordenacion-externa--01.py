import heapq

def crear_vueltas(datos, M):
    """Fase 1: trozos que si caben en memoria, ordenados de uno en uno."""
    return [sorted(datos[i:i + M]) for i in range(0, len(datos), M)]

datos = [7, 2, 5, 9, 1, 8, 3, 6, 4]
vueltas = crear_vueltas(datos, 3)
print("vueltas:", vueltas)                       # -> vueltas: [[2, 5, 7], [1, 8, 9], [3, 4, 6]]
print("cuantas vueltas:", len(vueltas))          # -> cuantas vueltas: 3

# Fase 2 con k = 2: cada ronda junta dos vueltas en una. heapq.merge mantiene un monticulo
# con la cabeza de cada vuelta, asi que en memoria solo hay k elementos, no las vueltas.
ronda_1 = list(heapq.merge(vueltas[0], vueltas[1]))
print("ronda 1:", ronda_1)                       # -> ronda 1: [1, 2, 5, 7, 8, 9]
ronda_2 = list(heapq.merge(ronda_1, vueltas[2]))
print("ronda 2:", ronda_2)                       # -> ronda 2: [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("rondas con k=2:", 2)                      # -> rondas con k=2: 2
print("igual que ordenar en memoria:", ronda_2 == sorted(datos))
# -> igual que ordenar en memoria: True
