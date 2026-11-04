def seleccion_actividades(intervalos):
    """Maximo numero de intervalos sin solapar. Criterio: el que antes termina."""
    ordenados = sorted(intervalos, key=lambda par: par[1])   # la clave es el fin
    elegidas, fin_ultimo = [], -1
    for inicio, fin in ordenados:
        if inicio >= fin_ultimo:                # compatible con la ultima elegida
            elegidas.append((inicio, fin))
            fin_ultimo = fin
    return elegidas

intervalos = [(0, 6), (1, 4), (3, 5), (5, 7), (3, 9), (5, 9),
              (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
elegidas = seleccion_actividades(intervalos)
print("cuantas caben:", len(elegidas))      # -> cuantas caben: 4
print("elegidas:", elegidas)                # -> elegidas: [(1, 4), (5, 7), (8, 11), (12, 16)]

# Criterio alternativo: la que antes empieza. Llega al mismo numero en este caso.
def por_inicio(intervalos):
    elegidas, fin_ultimo = [], -1
    for inicio, fin in sorted(intervalos):
        if inicio >= fin_ultimo:
            elegidas.append((inicio, fin)); fin_ultimo = fin
    return elegidas

print("por inicio:", por_inicio(intervalos))  # -> por inicio: [(0, 6), (6, 10), (12, 16)]
