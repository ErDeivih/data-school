import gc
import sys
import weakref

gc.disable()                             # decidimos nosotros cuando se libera la memoria

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

a, b = Nodo("a"), Nodo("b")
a.siguiente, b.siguiente = b, a          # ciclo: se apuntan el uno al otro
# Referencia debil: deja mirar el objeto sin contarle una referencia (no impide liberarlo).
vigilante = weakref.ref(a)

# getrefcount devuelve una referencia de mas: la del argumento que se acaba de pasar.
print("referencias a 'a':", sys.getrefcount(a))                  # -> 3
del a, b                                 # se sueltan las etiquetas; el ciclo sigue vivo
print("el ciclo sigue vivo:", vigilante() is not None)           # -> True
liberados = gc.collect()                 # el recolector generacional rompe el ciclo
print("objetos liberados:", liberados)                           # -> 2
print("ahora si esta libre:", vigilante() is None)               # -> True
gc.enable()                              # devolvemos el recolector automatico a su estado
