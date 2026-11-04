# No dirigido: cada arista aparece dos veces. El grado sale de la lista.
aristas = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]

adyacencia = {}
for u, v in aristas:                 # al no ser dirigido, se anota en los dos sentidos
    adyacencia.setdefault(u, []).append(v)
    adyacencia.setdefault(v, []).append(u)

grados = {v: len(vecinos) for v, vecinos in adyacencia.items()}
print("vecinos de C:", sorted(adyacencia["C"]))            # -> vecinos de C: ['A', 'B', 'D']
print("grados:", grados)                                   # -> grados: {'A': 2, 'B': 2, 'C': 3, 'D': 1}
print("suma de grados:", sum(grados.values()))             # -> suma de grados: 8
print("2 x aristas:", 2 * len(aristas))                    # -> 2 x aristas: 8
