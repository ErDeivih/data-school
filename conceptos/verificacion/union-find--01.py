class UnionFind:
    """Particion de 0..n-1 con union por rango y compresion de caminos."""

    def __init__(self, n):
        self.padre = list(range(n))       # al principio cada uno es su propia raiz
        self.rango = [0] * n              # cota de la altura del subarbol
        self.componentes = n

    def find(self, x):
        raiz = x
        while self.padre[raiz] != raiz:   # primera pasada: llegar a la raiz
            raiz = self.padre[raiz]
        while self.padre[x] != raiz:      # segunda pasada: colgar todos del camino de la raiz
            self.padre[x], x = raiz, self.padre[x]
        return raiz

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False                  # ya estaban juntos: no hay nada que fusionar
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx               # el arbol mas bajo cuelga del mas alto
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1           # solo crece la altura cuando empataban
        self.componentes -= 1
        return True

uf = UnionFind(6)
print("representantes al inicio:", [uf.find(i) for i in range(6)])  # -> representantes al inicio: [0, 1, 2, 3, 4, 5]

uf.union(0, 1)
uf.union(2, 3)
print("tras 0-1 y 2-3:", uf.padre, "conjuntos", uf.componentes)     # -> tras 0-1 y 2-3: [0, 0, 2, 2, 4, 5] conjuntos 4

uf.union(1, 3)
print("tras unir 1 y 3:", uf.padre, "conjuntos", uf.componentes)     # -> tras unir 1 y 3: [0, 0, 0, 2, 4, 5] conjuntos 3
print("mismo grupo (0, 3):", uf.find(0) == uf.find(3))               # -> mismo grupo (0, 3): True
print("mismo grupo (0, 4):", uf.find(0) == uf.find(4))               # -> mismo grupo (0, 4): False

uf.find(3)                                                          # la compresion aplana el camino
print("padre tras find(3):", uf.padre)                              # -> padre tras find(3): [0, 0, 0, 0, 4, 5]
