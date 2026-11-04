class Nodo:
    __slots__ = ("clave", "izq", "der")

    def __init__(self, clave):
        self.clave, self.izq, self.der = clave, None, None

def insertar(raiz, clave):
    if raiz is None:
        return Nodo(clave)
    if clave < raiz.clave:
        raiz.izq = insertar(raiz.izq, clave)
    elif clave > raiz.clave:
        raiz.der = insertar(raiz.der, clave)
    return raiz

def altura(raiz):
    if raiz is None:
        return -1
    return 1 + max(altura(raiz.izq), altura(raiz.der))

def comparaciones(raiz, objetivo):
    """Cuenta las comparaciones hasta encontrar la clave (o agotar el camino)."""
    n, actual = 0, raiz
    while actual is not None:
        n += 1
        if objetivo == actual.clave:
            return n
        actual = actual.izq if objetivo < actual.clave else actual.der
    return n

# Mismo conjunto de claves, dos ordenes de insercion
equilibrado = None
for k in (50, 30, 70, 20, 40, 60, 80):
    equilibrado = insertar(equilibrado, k)

degenerado = None
for k in (20, 30, 40, 50, 60, 70, 80):   # ya ordenadas: todas caen a la derecha
    degenerado = insertar(degenerado, k)

print("altura equilibrado:", altura(equilibrado))                  # -> altura equilibrado: 2
print("altura degenerado:", altura(degenerado))                    # -> altura degenerado: 6
print("comparaciones para el 80:", comparaciones(equilibrado, 80),
      comparaciones(degenerado, 80))                               # -> comparaciones para el 80: 3 7
