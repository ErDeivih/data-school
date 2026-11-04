# Recubrimiento de conjuntos voraz: cada paso, el conjunto con mas elementos nuevos.
universo = set(range(1, 7))
conjuntos = {"A": {1, 2, 3, 4}, "B": {1, 2, 5}, "C": {3, 4, 6}}


def voraz(universo, conjuntos):
    pendiente, elegidos = set(universo), []
    while pendiente:
        mejor = max(conjuntos, key=lambda s: len(conjuntos[s] & pendiente))
        if not (conjuntos[mejor] & pendiente):
            break                      # ningun conjunto cubre lo que queda
        elegidos.append(mejor)
        pendiente -= conjuntos[mejor]
    return elegidos


eleccion = voraz(universo, conjuntos)
print("voraz:", eleccion, "->", len(eleccion), "conjuntos")   # -> 3
print("optimo: B y C -> 2 conjuntos")
print("cociente observado: {:.2f}".format(len(eleccion) / 2))  # -> 1.50
print("cota teorica H(6) = {:.2f}".format(sum(1 / i for i in range(1, 7))))  # -> 2.45
