import sys
from itertools import permutations

sys.setrecursionlimit(20000)   # la recursion baja por la altura, pero conviene no ir justo

class Nodo:
    __slots__ = ("clave", "izq", "der", "altura")

    def __init__(self, clave):
        self.clave, self.izq, self.der, self.altura = clave, None, None, 0

def altura(n):
    return -1 if n is None else n.altura   # el arbol vacio mide -1, por convenio

def actualizar(n):
    n.altura = 1 + max(altura(n.izq), altura(n.der))
    return n

def rotar_derecha(y):
    """El hijo izquierdo sube; el subarbol intermedio cambia de padre."""
    x = y.izq
    y.izq = x.der
    x.der = y
    actualizar(y)
    return actualizar(x)

def rotar_izquierda(x):
    y = x.der
    x.der = y.izq
    y.izq = x
    actualizar(x)
    return actualizar(y)

def factor(n):
    return altura(n.izq) - altura(n.der)

def insertar_avl(nodo, clave):
    if nodo is None:
        return Nodo(clave)
    if clave < nodo.clave:
        nodo.izq = insertar_avl(nodo.izq, clave)
    elif clave > nodo.clave:
        nodo.der = insertar_avl(nodo.der, clave)
    else:
        return nodo
    actualizar(nodo)
    f = factor(nodo)
    if f > 1 and clave < nodo.izq.clave:        # izquierda-izquierda
        return rotar_derecha(nodo)
    if f < -1 and clave > nodo.der.clave:       # derecha-derecha
        return rotar_izquierda(nodo)
    if f > 1 and clave > nodo.izq.clave:        # izquierda-derecha: dos rotaciones
        nodo.izq = rotar_izquierda(nodo.izq)
        return rotar_derecha(nodo)
    if f < -1 and clave < nodo.der.clave:       # derecha-izquierda: dos rotaciones
        nodo.der = rotar_derecha(nodo.der)
        return rotar_izquierda(nodo)
    return nodo

def en_orden(nodo):
    if nodo is None:
        return []
    return en_orden(nodo.izq) + [nodo.clave] + en_orden(nodo.der)

avl = None
for k in (10, 20, 30):
    avl = insertar_avl(avl, k)
print("AVL tras 10,20,30:", en_orden(avl), "altura", avl.altura)   # -> AVL tras 10,20,30: [10, 20, 30] altura 1

avl = None
for k in (10, 30, 20):
    avl = insertar_avl(avl, k)
print("AVL tras 10,30,20:", en_orden(avl), "altura", avl.altura)   # -> AVL tras 10,30,20: [10, 20, 30] altura 1

avl = None
for k in range(1, 7):                  # claves ya ordenadas: el peor caso de un BST
    avl = insertar_avl(avl, k)
print("AVL con 1..6 ordenadas: altura", avl.altura)                # -> AVL con 1..6 ordenadas: altura 2
