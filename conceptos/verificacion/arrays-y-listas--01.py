import sys

# Una lista de Python guarda punteros: el contenedor y los objetos viven separados.
lista = list(range(1000))
print("contenedor de 1000 elementos (bytes):", sys.getsizeof(lista))  # -> contenedor de 1000 elementos (bytes): 8056
print("un entero suelto (bytes):", sys.getsizeof(1))                  # -> un entero suelto (bytes): 28
print("8 bytes por puntero, 1000 punteros:", 8 * 1000 + 56)           # -> 8 bytes por puntero, 1000 punteros: 8056
