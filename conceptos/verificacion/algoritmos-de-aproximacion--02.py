# Vertex cover 2-aproximado: emparejamiento maximal y a tomar los dos extremos.
aristas = [(1, 2), (1, 3), (2, 4), (5, 6), (6, 7)]
emparejamiento, cubiertos = [], set()
for u, v in aristas:
    if u not in cubiertos and v not in cubiertos:
        emparejamiento.append((u, v))
        cubiertos |= {u, v}

print("emparejamiento maximal:", emparejamiento)
print("vertex cover:", sorted(cubiertos), "->", len(cubiertos), "vertices")
print("cota inferior (tamano del emparejamiento):", len(emparejamiento))
# el cociente es 4 / 2 = 2, justo el factor garantizado
