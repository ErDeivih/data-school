# El ciclo rojo-verde escrito como script: primero la expectativa, luego la funcion.
def es_bisiesto(anio):
    # Los dos divisores cuentan: 1900 es divisible por 4 y por 100, asi que no es bisiesto.
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)

casos = [(2024, True), (2023, False), (1900, False), (2000, True)]
# Desempaquetado de la tupla en el for: cada vuelta deja anio y esperado ya separados.
for anio, esperado in casos:
    obtenido = es_bisiesto(anio)
    # is compara con el True/False de verdad; == daria por bueno un 1 y ocultaria un fallo.
    assert obtenido is esperado, f"falla {anio}: esperaba {esperado} y da {obtenido}"
    print(f"{anio}: {obtenido}")

print("casos comprobados:", len(casos))     # -> 4
