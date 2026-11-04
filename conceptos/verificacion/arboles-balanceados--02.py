from itertools import permutations

class NodoBST:
    __slots__ = ("clave", "izq", "der")

    def __init__(self, clave):
        self.clave, self.izq, self.der = clave, None, None

def altura_libre(n):
    if n is None:
        return -1
    return 1 + max(altura_libre(n.izq), altura_libre(n.der))

def altura_bst_ingenuo(claves):
    """BST sin reequilibrar: la altura depende del orden de llegada."""
    raiz = None
    for c in claves:
        nuevo = NodoBST(c)
        if raiz is None:
            raiz = nuevo
            continue
        actual = raiz
        while True:
            if c < actual.clave:
                if actual.izq is None:
                    actual.izq = nuevo
                    break
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nuevo
                    break
                actual = actual.der
    return altura_libre(raiz)

claves = list(range(1, 7))          # 720 ordenes de insercion distintos
alturas = [altura_bst_ingenuo(p) for p in permutations(claves)]

print("permutaciones:", len(alturas))                            # -> permutaciones: 720
print("altura minima:", min(alturas))                            # -> altura minima: 2
print("altura maxima:", max(alturas))                            # -> altura maxima: 5
print("altura media:", round(sum(alturas) / len(alturas), 2))     # -> altura media: 3.27
print("degenerados (altura 5):", sum(1 for h in alturas if h == 5))  # -> degenerados (altura 5): 32
