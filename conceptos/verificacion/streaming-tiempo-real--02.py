# Por que "al menos una vez" obliga a que el destino sea idempotente.
def insertar(destino, clave, valor):
    destino.append((clave, valor))

def merge(destino, clave, valor):
    destino[:] = [(k, v) for k, v in destino if k != clave]
    destino.append((clave, valor))

lote = [("a", 1), ("b", 2)]
reintento = [("b", 2), ("c", 3)]      # tras un fallo, el consumidor reprocesa desde su compensacion

con_insert = []
for par in lote + reintento:
    insertar(con_insert, *par)
print("con INSERT:", len(con_insert), "filas")        # -> con INSERT: 4 filas

con_merge = []
for par in lote + reintento:
    merge(con_merge, *par)
print("con MERGE:", len(con_merge), "filas")          # -> con MERGE: 3 filas
print("claves:", sorted(k for k, _ in con_merge))     # -> claves: ['a', 'b', 'c']
