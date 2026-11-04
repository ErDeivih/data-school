def mergesort(a):
    """Ordena por mezcla y devuelve (array ordenado, comparaciones)."""
    if len(a) <= 1:
        return a, 0
    medio = len(a) // 2
    izq, c1 = mergesort(a[:medio])
    der, c2 = mergesort(a[medio:])
    salida, i, j, c3 = [], 0, 0, 0
    while i < len(izq) and j < len(der):
        c3 += 1
        if izq[i] <= der[j]:        # <= y no <: asi la ordenacion es estable
            salida.append(izq[i]); i += 1
        else:
            salida.append(der[j]); j += 1
    return salida + izq[i:] + der[j:], c1 + c2 + c3

datos = [5, 2, 9, 1, 5, 6]
ordenado, comparaciones = mergesort(datos)
print("ordenado:", ordenado)                       # -> ordenado: [1, 2, 5, 5, 6, 9]
print("comparaciones:", comparaciones)             # -> comparaciones: 10
print("n log2 n aproximado:", round(6 * 2.585))    # -> n log2 n aproximado: 16
