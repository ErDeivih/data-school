# El argumento por defecto se evalua UNA vez, cuando se define la funcion
def acumula(x, caja=[]):
    caja.append(x)
    return caja

print("defecto mutable:", acumula(1), acumula(2), acumula(3))   # -> [1, 2, 3] [1, 2, 3] [1, 2, 3]

# La forma correcta: None por defecto y el contenedor se crea en cada llamada
def acumula_bien(x, caja=None):
    if caja is None:
        caja = []
    caja.append(x)
    return caja

print("con None:", acumula_bien(1), acumula_bien(2), acumula_bien(3))   # -> [1] [2] [3]
