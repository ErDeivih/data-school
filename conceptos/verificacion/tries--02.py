class Trie:
    def __init__(self):
        self.hijos = {}
        self.fin = False

    def insertar(self, palabra):
        nodo = self
        for c in palabra:
            nodo = nodo.hijos.setdefault(c, Trie())
        nodo.fin = True

def completar(raiz, prefijo):
    """Devuelve todas las palabras almacenadas que empiezan por el prefijo."""
    nodo = raiz
    for c in prefijo:
        if c not in nodo.hijos:
            return []
        nodo = nodo.hijos[c]
    resultados = []

    def recorrer(n, acumulado):
        if n.fin:
            resultados.append(prefijo + acumulado)
        for c, hijo in sorted(n.hijos.items()):
            recorrer(hijo, acumulado + c)

    recorrer(nodo, "")
    return resultados

def contar_nodos(raiz):
    return 1 + sum(contar_nodos(h) for h in raiz.hijos.values())

palabras = ["sol", "solo", "solar", "sal", "sarten"]
t = Trie()
for p in palabras:
    t.insertar(p)

print("completar 'sol':", completar(t, "sol"))    # -> completar 'sol': ['sol', 'solar', 'solo']
print("completar 'sa':", completar(t, "sa"))      # -> completar 'sa': ['sal', 'sarten']
print("completar 's':", completar(t, "s"))        # -> completar 's': ['sal', 'sarten', 'sol', 'solar', 'solo']
print("nodos del trie:", contar_nodos(t))         # -> nodos del trie: 13
print("caracteres guardados:", sum(len(p) for p in palabras))   # -> caracteres guardados: 21
