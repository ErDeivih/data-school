# Por que la compresion importa: contar los saltos de muchos find repetidos.
class UnionFind:
    def __init__(self, n, comprimir=True):
        self.padre = list(range(n))
        self.rango = [0] * n
        self.comprimir = comprimir
        self.saltos = 0

    def find(self, x):
        raiz = x
        while self.padre[raiz] != raiz:
            raiz = self.padre[raiz]
            self.saltos += 1
        if self.comprimir:
            while self.padre[x] != raiz:
                self.padre[x], x = raiz, self.padre[x]
        return raiz

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1

# Cadena degenerada a proposito: 0 <- 1 <- 2 <- ... <- n-1
def cadena(n, comprimir):
    uf = UnionFind(n, comprimir)
    for i in range(1, n):
        uf.padre[i] = i - 1        # se fuerza la cadena saltandose la union por rango
    uf.rango = [0] * n
    return uf

n = 500
for comprimir in (False, True):
    uf = cadena(n, comprimir)
    for _ in range(200):
        uf.find(n - 1)             # siempre el mismo extremo: el peor caso
    print("comprimir =", comprimir, "saltos totales:", uf.saltos)
    # -> comprimir = False saltos totales: 99800
    # -> comprimir = True saltos totales: 698
