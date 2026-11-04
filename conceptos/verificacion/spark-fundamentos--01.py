# Spark no cabe en este ejemplo, pero la pereza sí se puede reproducir.
datos = list(range(1, 1_000_001))
veces = {"filtro": 0, "map": 0}

def filtro(xs, cond):
    for x in xs:
        if cond(x):
            veces["filtro"] += 1     # solo se ejecuta al consumir el generador
            yield x

def doble(xs):
    for x in xs:
        veces["map"] += 1
        yield 2 * x

plan = doble(filtro(datos, lambda x: x % 7 == 0))
print("antes de la accion:", veces)     # -> antes de la accion: {'filtro': 0, 'map': 0}
total = sum(plan)                       # la accion recorre el plan entero, una sola vez
print("despues de la accion:", veces)   # -> despues de la accion: {'filtro': 142857, 'map': 142857}
print("suma:", total)                   # -> suma: 142857857142
