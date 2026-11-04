# Tiempo virtual: el reloj no aporta nada al ejemplo y asi el resultado es exacto.
reloj = {"t": 0.0}                  # un dict de un solo valor: asi se puede cambiar desde dentro
cache = {}
consultas = 0

def obtener_con_cache(clave, ttl=1.0):
    """Patron cache-aside: mira la cache, y solo si falla va al almacen."""
    global consultas
    entrada = cache.get(clave)      # .get devuelve None si no esta: no lanza KeyError
    if entrada and reloj["t"] - entrada[1] < ttl:
        # entrada[1] es la marca de tiempo; sin ella no se puede saber si ha caducado
        return entrada[0], "acierto"
    reloj["t"] += 0.2                       # la consulta a la base de datos tarda 200 ms
    consultas += 1
    cache[clave] = (f"fila-{clave}", reloj["t"])     # se guarda el valor CON su marca de tiempo
    return cache[clave][0], "fallo"                  # indice 0 = valor; el 1 es la marca

for clave in ["u1", "u1", "u1"]:
    _, estado = obtener_con_cache(clave)             # el guion bajo descarta el valor
    print(f"t={reloj['t']:.1f}s {clave} -> {estado}")

reloj["t"] = 2.0                            # pasa el tiempo de golpe: u1 ya ha caducado
print("tras el TTL:", obtener_con_cache("u1")[1])        # -> fallo
print("consultas al almacen:", consultas, "de 4 lecturas")
print("tiempo esperando al almacen:", round(0.2 * consultas, 1), "s")   # 0,2 s por consulta
