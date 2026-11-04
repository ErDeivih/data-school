# El merge por clave es idempotente: reprocesar el mismo lote no cambia el resultado.
def aplicar(destino, lote):
    copia = dict(destino)
    for lsn, op, clave, valor in lote:
        if op == "D":
            copia.pop(clave, None)
        else:
            copia[clave] = valor
    return copia

destino = {1: "ana", 2: "luis"}
lote = [(1040, "U", 1, "ana maria"), (1041, "I", 5, "pablo")]

una = aplicar(destino, lote)
dos = aplicar(una, lote)                      # el mismo lote, otra vez

print("idempotente:", una == dos)             # -> idempotente: True
print("claves tras dos pasadas:", sorted(dos))  # -> claves tras dos pasadas: [1, 2, 5]
