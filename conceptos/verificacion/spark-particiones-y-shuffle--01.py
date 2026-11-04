# Cuanto se reduce el shuffle segun la cardinalidad de la clave, con agregacion parcial.
filas = 200_000_000
bytes_por_fila = 100
particiones = 200

def barajado(filas, cardinalidad, particiones, bytes_por_fila):
    # El lado del mapa emite como mucho una fila por clave distinta y particion,
    # y nunca mas filas que las de entrada.
    claves_por_particion = min(cardinalidad, filas / particiones)
    filas_barajadas = min(filas, claves_por_particion * particiones)
    return filas_barajadas, filas_barajadas * bytes_por_fila / 1e9

for nombre, card in [("pais", 200), ("ciudad", 50_000), ("usuario", 20_000_000)]:
    n, gb = barajado(filas, card, particiones, bytes_por_fila)
    print(f"{nombre:<8} cardinalidad {card:>9,} -> {n:>12,.0f} filas, {gb:>8.4f} GB barajados")
