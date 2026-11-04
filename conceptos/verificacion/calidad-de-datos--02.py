# El mismo grupo de filas y dos claves de deduplicacion distintas: dos respuestas.
personas = [
    ("Ana Perez", "11111111H"),
    ("Ana Perez", "11111111H"),
    ("Ana Perez", "22222222J"),
]

def duplicados(filas, columna):
    """Filas repetidas de una clave: filas totales menos valores distintos de esa clave."""
    return len(filas) - len({fila[columna] for fila in filas})

print("filas", len(personas))   # -> filas 3
# Por nombre parecen tres la misma persona; por NIF solo hay una repetida de verdad.
print("duplicados por nombre ", duplicados(personas, 0))
# -> duplicados por nombre  2
print("duplicados por nif    ", duplicados(personas, 1))
# -> duplicados por nif     1
