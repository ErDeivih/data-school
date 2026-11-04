# Lo que un trie hace y una tabla hash no puede hacer barato: consultas por prefijo.
import time

class Trie:
    def __init__(self):
        self.hijos = {}
        self.fin = False

    def insertar(self, palabra):
        nodo = self
        for c in palabra:
            nodo = nodo.hijos.setdefault(c, Trie())
        nodo.fin = True

palabras = [f"palabra{i:05d}" for i in range(20000)]   # 20.000 claves con prefijo comun
t = Trie()
for p in palabras:
    t.insertar(p)
conjunto = set(palabras)

# Buscar un prefijo en el trie: bajar 7 caracteres, sin importar cuantas palabras haya.
inicio = time.perf_counter()
for _ in range(2000):
    nodo = t
    for c in "palabra0000":
        nodo = nodo.hijos[c]
micros_trie = (time.perf_counter() - inicio) / 2000 * 1e6

# Lo mismo con una tabla hash: hay que mirar todas las claves.
inicio = time.perf_counter()
for _ in range(2000):
    cuantas = [p for p in conjunto if p.startswith("palabra0000")]
micros_hash = (time.perf_counter() - inicio) / 2000 * 1e6

print(f"prefijo en trie: {micros_trie:7.1f} us")
print(f"prefijo en hash: {micros_hash:7.1f} us")
print("el trie es mas rapido:", micros_trie < micros_hash)   # -> el trie es mas rapido: True
print("cuantas palabras empiezan igual:", len(cuantas))      # -> cuantas palabras empiezan igual: 10
