# Reproduccion minima del fallo, en seis lineas y sin el proyecto entero.
def total_por_columna(filas, columna):
    return sum(fila[columna] for fila in filas)

filas = [{"pais": "ES", "importe": 3}, {"pais": "PT", "importe": 5}]
print(f"suma de importe: {total_por_columna(filas, 'importe')}")

try:
    total_por_columna(filas, "moneda")
except KeyError as exc:
    print(f"falla con {type(exc).__name__}: {exc}")
