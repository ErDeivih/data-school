# Reemplazar condicionales anidados por una tabla: mismo resultado, menos ramas que probar.
def tasa_vieja(tipo):
    # Cadena de elif: cada rama es un camino que hay que probar por separado.
    if tipo == "basica":
        return 0.04
    elif tipo == "plus":
        return 0.02
    elif tipo == "premium":
        return 0.01
    else:
        return 0.06                 # el else final es el valor por defecto

TASAS = {"basica": 0.04, "plus": 0.02, "premium": 0.01}
POR_DEFECTO = 0.06                  # mismo numero que el else, pero ahora con nombre

def tasa_nueva(tipo):
    # get con segundo argumento: devuelve el valor por defecto en vez de dar KeyError.
    return TASAS.get(tipo, POR_DEFECTO)

for tipo in ["basica", "plus", "premium", "desconocida"]:
    # La prueba compara las dos versiones para cada tipo, incluido el que no esta en la tabla.
    assert tasa_vieja(tipo) == tasa_nueva(tipo), f"difieren en {tipo}"
    print(f"{tipo:<12} {tasa_nueva(tipo):.2f}")

# +1 porque tambien se comprueba el tipo de fuera de la tabla (el valor por defecto).
print("tipos comprobados:", len(TASAS) + 1)        # -> 4
