# Registro de transacciones: cada version anade y quita ficheros, nada se edita en el sitio
snapshots = [
    {"v": 1, "anade": ["f1", "f2", "f3"], "quita": []},
    {"v": 2, "anade": ["f4"], "quita": ["f1"]},   # actualiza las filas 1..100
    {"v": 3, "anade": ["f5"], "quita": ["f4"]},   # borra las filas 1..50
]
# Cada fichero guarda pares (id, importe); f4 es la version actualizada de f1
ficheros = {
    "f1": [(i, i * 10.0) for i in range(1, 101)],
    "f2": [(i, i * 10.0) for i in range(101, 201)],
    "f3": [(i, i * 10.0) for i in range(201, 301)],
    "f4": [(i, i * 12.0) for i in range(1, 101)],
    "f5": [(i, i * 12.0) for i in range(51, 101)],
}

def vivos(version):
    conjunto = set()
    for s in snapshots:
        if s["v"] > version:
            break
        conjunto |= set(s["anade"])       # un commit solo anade y quita referencias
        conjunto -= set(s["quita"])
    return sorted(conjunto)

for v in (1, 2, 3):
    filas = [fila for f in vivos(v) for fila in ficheros[f]]
    total = sum(imp for _, imp in filas)
    print(f"v{v}: {len(vivos(v))} ficheros, {len(filas)} filas, importe {total:.0f}")
# -> v1: 3 ficheros, 300 filas, importe 451500
# -> v2: 3 ficheros, 300 filas, importe 461600
# -> v3: 3 ficheros, 250 filas, importe 446300
