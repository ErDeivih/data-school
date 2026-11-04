# El parche: comprobar antes y decir que columnas hay disponibles.
def total_por_columna(filas, columna):
    disponibles = sorted({clave for fila in filas for clave in fila})
    if columna not in disponibles:
        raise ValueError(f"columna '{columna}' no existe; disponibles: {disponibles}")
    return sum(fila[columna] for fila in filas)

filas = [{"pais": "ES", "importe": 3}, {"pais": "PT", "importe": 5}]
try:
    total_por_columna(filas, "moneda")
except ValueError as exc:
    print(f"ahora falla con ValueError: {exc}")
