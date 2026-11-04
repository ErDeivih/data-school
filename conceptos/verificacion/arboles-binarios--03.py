# Consulta por rango: lo que un BST hace y una tabla hash no puede hacer sin ordenar antes.
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

def rango(raiz, a, b, visitados=None):
    """Devuelve las claves en [a, b] podando las ramas que quedan fuera."""
    visitados = [0] if visitados is None else visitados
    if raiz is None:
        return []
    visitados[0] += 1
    if raiz.clave < a:                       # todo el subarbol izquierdo es menor que a
        return rango(raiz.der, a, b, visitados)
    if raiz.clave > b:                       # todo el subarbol derecho es mayor que b
        return rango(raiz.izq, a, b, visitados)
    return rango(raiz.izq, a, b, visitados) + [raiz.clave] + rango(raiz.der, a, b, visitados)

claves = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90]
raiz = None
for k in claves:
    raiz = insertar(raiz, k)

recorridos = [0]
print("claves entre 30 y 60:", rango(raiz, 30, 60, recorridos))  # -> claves entre 30 y 60: [30, 35, 40, 45, 50, 55, 60]
print("nodos visitados:", recorridos[0], "de", len(claves))     # -> nodos visitados: 11 de 15
