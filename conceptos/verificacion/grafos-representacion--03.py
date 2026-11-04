# Cuidado con las aristas repetidas: el mismo par anotado dos veces rompe la identidad.
aristas = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("A", "B")]  # (A,B) esta dos veces

adyacencia = {}
for u, v in aristas:
    adyacencia.setdefault(u, []).append(v)
    adyacencia.setdefault(v, []).append(u)

grados = {v: len(vecinos) for v, vecinos in adyacencia.items()}
print("vecinos de A:", sorted(adyacencia["A"]))            # -> vecinos de A: ['B', 'B', 'C']
print("suma de grados:", sum(grados.values()))             # -> suma de grados: 10
print("aristas distintas:", len(set(map(frozenset, aristas))))  # -> aristas distintas: 4
