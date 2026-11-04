class Nodo:
    __slots__ = ("clave", "izq", "der")

    def __init__(self, clave):
        self.clave, self.izq, self.der = clave, None, None

def insertar(raiz, clave):
    """Inserta respetando la propiedad BST y devuelve la raiz del subarbol."""
    if raiz is None:
        return Nodo(clave)
    if clave < raiz.clave:
        raiz.izq = insertar(raiz.izq, clave)
    elif clave > raiz.clave:
        raiz.der = insertar(raiz.der, clave)
    return raiz   # clave duplicada: se ignora a proposito

def en_orden(raiz):
    """Izquierda, nodo, derecha: en un BST sale ordenado."""
    if raiz is None:
        return []
    return en_orden(raiz.izq) + [raiz.clave] + en_orden(raiz.der)

def altura(raiz):
    if raiz is None:
        return -1                      # el arbol vacio tiene altura -1 por convenio
    return 1 + max(altura(raiz.izq), altura(raiz.der))

raiz = None
for k in (50, 30, 70, 20, 40, 60, 80):
    raiz = insertar(raiz, k)

print("en orden:", en_orden(raiz))   # -> en orden: [20, 30, 40, 50, 60, 70, 80]
print("altura:", altura(raiz))       # -> altura: 2
