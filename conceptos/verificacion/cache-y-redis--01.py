from collections import OrderedDict

CAPACIDAD = 3
cache = OrderedDict()                # hace falta el orden: hay que saber cual es el mas antiguo
aciertos = fallos = 0                # asignacion encadenada: los dos nombres empiezan en cero

def obtener(clave):
    global aciertos, fallos          # sin global, += crearia variables locales y no subiria el total
    if clave in cache:
        cache.move_to_end(clave)          # LRU: lo usado va al final
        aciertos += 1
        return cache[clave]
    fallos += 1
    valor = f"valor-de-{clave}"      # simula el calculo caro: aqui iria la consulta a la base
    cache[clave] = valor
    if len(cache) > CAPACIDAD:       # el desalojo se comprueba DESPUES de insertar
        cache.popitem(last=False)         # se desaloja el menos usado recientemente
    return valor

for clave in ["a", "b", "c", "a", "d", "a", "b"]:
    obtener(clave)
    print(f"pido {clave} -> cache {list(cache)}")   # list() muestra el orden: del mas viejo al mas nuevo

print("aciertos", aciertos, "fallos", fallos)
print("tasa de acierto", round(aciertos / (aciertos + fallos), 2))   # la division con / da float
