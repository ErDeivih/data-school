# Dos politicas de crecimiento del mismo array: duplicar o sumar un hueco.
def copias_totales(n, politica):
    capacidad, tam, copias = 1, 0, 0
    for _ in range(n):
        if tam == capacidad:                  # no cabe: hay que ampliar
            copias += tam                     # se traslada todo lo guardado
            capacidad = capacidad * 2 if politica == "doble" else capacidad + 1
        tam += 1
    return copias

for n in (8, 16, 32, 1024):
    print(f"n={n:>5}  duplicando {copias_totales(n, 'doble'):>8}  "
          f"sumando uno {copias_totales(n, 'uno'):>8}")

# La comprobacion que importa: con duplicacion las copias son n-1, muy por debajo de 2n
print("copias con n=1024 y duplicacion:", copias_totales(1024, "doble"))   # -> 1023
print("copias con n=100000 y duplicacion:", copias_totales(100000, "doble"))  # -> 131071
