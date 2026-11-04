import zlib

def repartir(filas, P):
    """Reparte por hash de la clave: la misma clave cae siempre en la misma particion."""
    partes = [[] for _ in range(P)]
    for fila in filas:
        partes[zlib.crc32(str(fila[0]).encode()) % P].append(fila)
    return partes

# Ojo: hash() de Python cambia en cada ejecucion para las cadenas (PYTHONHASHSEED), asi
# que para medir y comparar hace falta una funcion fija como crc32.
P, memoria = 8, 2000
uniforme = [(i % 5000, i) for i in range(10000)]                    # 5000 claves, 2 filas cada una
sesgado = [(42 if i % 2 == 0 else i % 5000, i) for i in range(10000)]   # la clave 42 en la mitad

for nombre, filas in (("uniforme", uniforme), ("sesgado ", sesgado)):
    tamanos = [len(p) for p in repartir(filas, P)]
    print(nombre, "mayor particion:", max(tamanos), "cabe en memoria:", max(tamanos) <= memoria)
# -> uniforme mayor particion: 1252 cabe en memoria: True
# -> sesgado  mayor particion: 5624 cabe en memoria: False

print("con P = 64, uniforme:", max(len(p) for p in repartir(uniforme, 64)))
# -> con P = 64, uniforme: 166
print("con P = 64, sesgado:", max(len(p) for p in repartir(sesgado, 64)))
# -> con P = 64, sesgado: 5076
