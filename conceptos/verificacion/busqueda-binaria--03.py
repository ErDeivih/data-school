# Busqueda lineal contra binaria: el mismo array, el peor caso de cada una.
def lineal(a, x):
    comparaciones = 0
    for i, v in enumerate(a):
        comparaciones += 1
        if v == x:
            return i, comparaciones
    return -1, comparaciones

def binaria(a, x):
    izq, der, comparaciones = 0, len(a) - 1, 0
    while izq <= der:
        medio = (izq + der) // 2
        comparaciones += 1
        if a[medio] == x:
            return medio, comparaciones
        if a[medio] < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1, comparaciones

datos = list(range(0, 2000, 2))       # 1000 numeros pares ordenados
objetivo = 1998                       # el ultimo: peor caso para las dos
print("lineal ", lineal(datos, objetivo))    # -> lineal  (999, 1000)
print("binaria", binaria(datos, objetivo))   # -> binaria (999, 10)
