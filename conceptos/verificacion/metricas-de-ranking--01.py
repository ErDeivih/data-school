import numpy as np

# Dos consultas: 1 si el documento de esa posicion era relevante
consulta_a = np.array([1, 0, 1, 0, 1])
consulta_b = np.array([0, 1, 0, 0, 0])

def ap(rel):
    """Precision media: promedio de la precision en cada acierto."""
    aciertos, suma = 0, 0.0
    # start=1 porque la posicion de la lista empieza en 1: con start=0 el primer
    # acierto dividiria entre cero y Python lanzaria ZeroDivisionError.
    for i, r in enumerate(rel, start=1):
        if r == 1:
            aciertos += 1
            suma += aciertos / i
    return suma / rel.sum()      # numpy.int64: la division ya da float

print(f"precision@3 A {consulta_a[:3].sum() / 3:.4f}")                # -> 0.6667
print(f"recall@3 A    {consulta_a[:3].sum() / consulta_a.sum():.3f}") # -> 0.667
print(f"AP A {ap(consulta_a):.4f}  AP B {ap(consulta_b):.4f}")        # -> AP A 0.7556  AP B 0.5000
print(f"MAP {(ap(consulta_a) + ap(consulta_b)) / 2:.4f}")             # -> 0.6278
print(f"MRR {(1 / 1 + 1 / 2) / 2:.4f}")                               # -> 0.7500
