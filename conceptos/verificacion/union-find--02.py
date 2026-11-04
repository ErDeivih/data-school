# Kruskal: el arbol de expansion minimo. Union-find decide que aristas no cierran ciclo.
class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))
        self.rango = [0] * n

    def find(self, x):
        while self.padre[x] != x:
            self.padre[x] = self.padre[self.padre[x]]   # compresion en una pasada
            x = self.padre[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1
        return True

n = 6
aristas = [(0, 1, 4), (0, 2, 4), (0, 3, 1), (1, 2, 2), (1, 4, 3),
           (2, 3, 5), (2, 5, 6), (3, 4, 1), (4, 5, 2)]

uf = UnionFind(n)
total, arbol = 0, []
for u, v, w in sorted(aristas, key=lambda a: a[2]):   # de menor a mayor peso
    if uf.union(u, v):                                # union devuelve False si ya estaban juntos
        arbol.append((u, v, w))
        total += w

print("aristas del arbol:", arbol)      # -> aristas del arbol: [(0, 3, 1), (3, 4, 1), (1, 2, 2), (4, 5, 2), (1, 4, 3)]
print("peso total:", total)             # -> peso total: 9
print("aristas descartadas:", len(aristas) - len(arbol))  # -> aristas descartadas: 4
