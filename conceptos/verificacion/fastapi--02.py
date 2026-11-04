llamadas = 0

def get_db():
    """Dependencia cara: abrir conexion. FastAPI la cachea dentro de la misma peticion."""
    global llamadas                       # sin global, llamadas += 1 seria una variable local
    llamadas += 1
    return {"conexion": llamadas}

def manejar_peticion(usar_cache=True):
    cache = {}                            # diccionario nuevo: la cache no sobrevive a la peticion
    def dep(nombre):
        if not usar_cache or nombre not in cache:
            cache[nombre] = get_db()      # solo se abre la conexion la primera vez que se pide
        return cache[nombre]
    return dep("db"), dep("db"), dep("db")   # las tres devuelven el MISMO objeto

antes = llamadas
db1, db2, db3 = manejar_peticion(usar_cache=True)
print("misma peticion, 3 usos:", db1 is db2 is db3, "->", llamadas - antes, "apertura")   # -> True -> 1 apertura
# is compara identidad (el mismo objeto), no igualdad: es justo lo que se quiere comprobar

antes = llamadas
manejar_peticion(usar_cache=False)
print("dependencia no cacheada:", llamadas - antes, "aperturas")                          # -> 3 aperturas
