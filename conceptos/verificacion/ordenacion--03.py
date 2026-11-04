# Estabilidad: mismo criterio de orden, distinto orden relativo de los empates.
personas = [("ana", 30), ("luis", 25), ("marta", 30), ("pablo", 25)]

def insercion_estable(a, clave):
    """Insercion con clave: al mover solo si es estrictamente mayor, empates no se tocan."""
    a = a[:]
    for i in range(1, len(a)):
        actual, j = a[i], i - 1
        while j >= 0 and clave(a[j]) > clave(actual):   # > y no >=: por eso es estable
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual
    return a

por_edad = insercion_estable(personas, lambda p: p[1])
print("estable:", por_edad)
# -> estable: [('luis', 25), ('pablo', 25), ('ana', 30), ('marta', 30)]
print("mismo resultado que sorted:", por_edad == sorted(personas, key=lambda p: p[1]))
# -> mismo resultado que sorted: True
