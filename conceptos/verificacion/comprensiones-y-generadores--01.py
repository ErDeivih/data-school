import sys

# Lista por comprension: se calcula y se guarda todo de golpe
cuadrados_lista = [x * x for x in range(1_000_000)]
# Expresion generadora: NO calcula nada hasta que se lo pides
cuadrados_gen = (x * x for x in range(1_000_000))

print("lista:", sys.getsizeof(cuadrados_lista))          # -> lista: 8448728
print("generador:", sys.getsizeof(cuadrados_gen))        # -> generador: 200
print("primeros tres:", [next(cuadrados_gen) for _ in range(3)])   # -> primeros tres: [0, 1, 4]

# Diccionario por comprension: de nombre a lista de precios
filas = [("pan", 3.5), ("vino", 9.0), ("pan", 2.0)]
por_categoria = {c: [v for n, v in filas if n == c] for c in {n for n, _ in filas}}
print("categorias:", sorted(por_categoria))              # -> categorias: ['pan', 'vino']
print("pan:", por_categoria["pan"])                      # -> pan: [3.5, 2.0]
