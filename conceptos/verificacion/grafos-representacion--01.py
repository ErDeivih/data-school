# Las dos representaciones del mismo grafo dirigido y ponderado.
aristas = [("A", "B", 4), ("A", "C", 2), ("B", "C", 5), ("B", "D", 10),
           ("C", "E", 3), ("E", "D", 4), ("D", "A", 11)]

vertices = ["A", "B", "C", "D", "E"]
indice = {v: i for i, v in enumerate(vertices)}      # nombre -> posicion en la matriz

# Lista de adyacencia: solo se guarda lo que existe
adyacencia = {v: [] for v in vertices}
for u, v, w in aristas:
    adyacencia[u].append((v, w))

# Matriz de adyacencia: n x n celdas, casi todas vacias
n = len(vertices)
matriz = [[0] * n for _ in range(n)]
for u, v, w in aristas:
    matriz[indice[u]][indice[v]] = w

print("lista de A:", adyacencia["A"])                     # -> lista de A: [('B', 4), ('C', 2)]
print("celdas de la matriz:", n * n)                      # -> celdas de la matriz: 25
print("entradas de la lista:", sum(len(x) for x in adyacencia.values()))  # -> entradas de la lista: 7
print("peso de B a D por matriz:", matriz[indice["B"]][indice["D"]])      # -> peso de B a D por matriz: 10
print("peso de D a B (no existe):", matriz[indice["D"]][indice["B"]])     # -> peso de D a B (no existe): 0
