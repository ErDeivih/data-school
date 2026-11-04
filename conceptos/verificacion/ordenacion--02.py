def quicksort_lomuto(a):
    """Quicksort con pivote en el ultimo elemento. Devuelve (ordenado, comparaciones)."""
    a = a[:]
    comparaciones = [0]

    def ordenar(izq, der):
        if izq >= der:
            return
        pivote = a[der]
        i = izq
        for j in range(izq, der):       # particion de Lomuto
            comparaciones[0] += 1
            if a[j] <= pivote:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[der] = a[der], a[i]     # el pivote va a su sitio definitivo
        ordenar(izq, i - 1)
        ordenar(i + 1, der)

    ordenar(0, len(a) - 1)
    return a, comparaciones[0]

aleatorio = [5, 2, 9, 1, 5, 6]
ya_ordenado = [1, 2, 3, 4, 5]
print("aleatorio:", quicksort_lomuto(aleatorio))       # -> aleatorio: ([1, 2, 5, 5, 6, 9], 11)
print("ya ordenado:", quicksort_lomuto(ya_ordenado))   # -> ya ordenado: ([1, 2, 3, 4, 5], 10)
print("cuadratico para n=5:", 5 * 4 // 2)              # -> cuadratico para n=5: 10
