import itertools

# Perezoso: el rango es infinito y no se materializa nada hasta que se pide
pares = (x for x in itertools.count() if x % 2 == 0)
print("cinco pares:", list(itertools.islice(pares, 5)))     # -> cinco pares: [0, 2, 4, 6, 8]

# Un fichero de texto tambien es un iterador: se recorre linea a linea
lineas = ["a,1", "b,2", "c,3"]
pares_clave_valor = {clave: int(valor) for clave, valor in (l.split(",") for l in lineas)}
print("leido:", pares_clave_valor)                          # -> leido: {'a': 1, 'b': 2, 'c': 3}

# Un generador agotado no se reinicia: la segunda vuelta devuelve una lista vacia
agotado = (n for n in range(3))
print("primera vuelta:", list(agotado))                     # -> primera vuelta: [0, 1, 2]
print("segunda vuelta:", list(agotado))                     # -> segunda vuelta: []
