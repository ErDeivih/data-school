def busqueda_binaria(a, x):
    """Devuelve el indice de x en el array ordenado a, o -1 si no esta."""
    izq, der = 0, len(a) - 1
    while izq <= der:                 # el rango es cerrado: [izq, der]
        medio = (izq + der) // 2
        if a[medio] == x:
            return medio
        if a[medio] < x:
            izq = medio + 1           # medio ya esta comprobado: se descarta
        else:
            der = medio - 1
    return -1                          # el rango se vacio: no esta

a = [3, 7, 11, 18, 24, 31, 42, 56]
print("indice de 31:", busqueda_binaria(a, 31))   # -> indice de 31: 5
print("indice de 20:", busqueda_binaria(a, 20))   # -> indice de 20: -1
print("indice de 3:", busqueda_binaria(a, 3))     # -> indice de 3: 0
