def mergesort_contando(a):
    """Mergesort que devuelve (ordenado, comparaciones) y permite ver la recursion."""
    if len(a) <= 1:
        return a, 0
    medio = len(a) // 2
    izq, c1 = mergesort_contando(a[:medio])
    der, c2 = mergesort_contando(a[medio:])
    salida, i, j, c3 = [], 0, 0, 0
    while i < len(izq) and j < len(der):
        c3 += 1
        if izq[i] <= der[j]:
            salida.append(izq[i]); i += 1
        else:
            salida.append(der[j]); j += 1
    return salida + izq[i:] + der[j:], c1 + c2 + c3

datos = [38, 27, 43, 3, 9, 82, 10, 1]
ordenado, comparaciones = mergesort_contando(datos)
print("ordenado:", ordenado)
# -> ordenado: [1, 3, 9, 10, 27, 38, 43, 82]
print("comparaciones:", comparaciones, "de un maximo teorico de", 8 * 3)   # -> comparaciones: 17 de un maximo teorico de 24
print("niveles de particion:", 3)                                          # -> niveles de particion: 3
