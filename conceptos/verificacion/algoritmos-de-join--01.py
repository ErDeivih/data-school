def bucle_anidado(A, B, clave):
    """Compara cada fila de A con todas las de B: n_A por n_B comparaciones."""
    pares, comparaciones = [], 0
    for a in A:
        for b in B:
            comparaciones += 1
            if clave(a) == clave(b):
                pares.append((clave(a), a[1], b[1]))
    return sorted(pares), comparaciones

def hash_join(A, B, clave):
    """Construye la tabla hash con B y sondea con A: una busqueda por fila de A."""
    indice = {}
    for b in B:
        indice.setdefault(clave(b), []).append(b)    # las claves repetidas se acumulan
    pares, busquedas = [], 0
    for a in A:
        busquedas += 1
        for b in indice.get(clave(a), []):
            pares.append((clave(a), a[1], b[1]))
    return sorted(pares), busquedas

def sort_merge(A, B, clave):
    """Ordena las dos entradas y las recorre en paralelo, como una cremallera."""
    A, B = sorted(A, key=clave), sorted(B, key=clave)
    pares, i, j, comparaciones = [], 0, 0, 0
    while i < len(A) and j < len(B):
        comparaciones += 1
        ca, cb = clave(A[i]), clave(B[j])
        if ca == cb:                    # hay que emparejar con TODOS los empatados de B
            k = j
            while k < len(B) and clave(B[k]) == ca:
                pares.append((ca, A[i][1], B[k][1])); k += 1
            i += 1
        elif ca < cb:
            i += 1
        else:
            j += 1
    return sorted(pares), comparaciones

clientes = [(1, "ana"), (2, "luis"), (3, "marta")]
pedidos = [(3, "cafe"), (1, "te"), (3, "pan"), (2, "agua"), (1, "sal")]
clave = lambda fila: fila[0]
print("bucle anidado:", bucle_anidado(pedidos, clientes, clave)[1], "comparaciones")
# -> bucle anidado: 15 comparaciones
print("hash join:", hash_join(pedidos, clientes, clave)[1], "busquedas")
# -> hash join: 5 busquedas
print("sort-merge:", sort_merge(pedidos, clientes, clave)[1], "comparaciones")
# -> sort-merge: 7 comparaciones
a = bucle_anidado(pedidos, clientes, clave)[0]
b = hash_join(pedidos, clientes, clave)[0]
c = sort_merge(pedidos, clientes, clave)[0]
print("los tres dan lo mismo:", a == b == c)     # -> los tres dan lo mismo: True
print("filas del resultado:", len(a))            # -> filas del resultado: 5
