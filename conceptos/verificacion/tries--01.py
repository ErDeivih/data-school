class Trie:
    """Trie con hijos en diccionario: menos memoria que un array por alfabeto."""

    def __init__(self):
        self.hijos = {}          # caracter -> subtrie
        self.fin = False         # True si el camino hasta aqui es una palabra completa

    def insertar(self, palabra):
        nodo = self
        for c in palabra:
            nodo = nodo.hijos.setdefault(c, Trie())
        nodo.fin = True          # sin esta marca, "casa" y "casar" serian indistinguibles

    def contiene(self, palabra):
        nodo = self
        for c in palabra:
            if c not in nodo.hijos:
                return False
            nodo = nodo.hijos[c]
        return nodo.fin         # existe el camino, pero puede ser solo un prefijo

    def empieza_por(self, prefijo):
        nodo = self
        for c in prefijo:
            if c not in nodo.hijos:
                return False
            nodo = nodo.hijos[c]
        return True             # aqui si basta con que exista el nodo

t = Trie()
for palabra in ("sol", "solo", "solar", "sal", "sarten"):
    t.insertar(palabra)

print("contiene sol:", t.contiene("sol"))        # -> contiene sol: True
print("contiene so:", t.contiene("so"))          # -> contiene so: False
print("prefijo so:", t.empieza_por("so"))        # -> prefijo so: True
print("prefijo sor:", t.empieza_por("sor"))      # -> prefijo sor: False
print("contiene sar:", t.contiene("sar"))        # -> contiene sar: False
