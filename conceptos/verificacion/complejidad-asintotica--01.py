# Contamos comparaciones en vez de segundos: el cronometro depende de la maquina,
# el conteo de operaciones no.
datos = list(range(0, 2 ** 20, 2))          # 524288 numeros pares ordenados
objetivo = 900000                            # esta en la posicion 450000

def lineal(v, x):
    for i, y in enumerate(v):                # recorre hasta encontrarlo
        if y == x:
            return i, i + 1
    return -1, len(v)

def binaria(v, x):
    lo, hi, comps = 0, len(v) - 1, 0
    while lo <= hi:
        medio = (lo + hi) // 2               # parte el espacio de busqueda por la mitad
        comps += 1
        if v[medio] == x:
            return medio, comps
        if v[medio] < x:
            lo = medio + 1
        else:
            hi = medio - 1
    return -1, comps

print("elementos en la lista ", len(datos))               # -> elementos en la lista  524288
print("comparaciones lineal  ", lineal(datos, objetivo)[1])   # -> comparaciones lineal   450001
print("comparaciones binaria ", binaria(datos, objetivo)[1])  # -> comparaciones binaria  19
