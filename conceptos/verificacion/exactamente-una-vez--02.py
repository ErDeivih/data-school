# La clave se comprueba y se apunta en la misma operacion atomica. Aqui lo simulamos
# con un conjunto, que es lo que en produccion seria un indice unico en la base de datos.
def procesar(estado, clave):
    if clave in estado["vistas"]:
        return False               # ya aplicado: confirmamos y no repetimos el efecto
    # El orden importa: primero se apunta la clave y despues se aplica el efecto, y en
    # produccion las dos escrituras van en la misma transaccion.
    estado["vistas"].add(clave)
    estado["cobros"] += 1
    return True

estado = {"vistas": set(), "cobros": 0}
for clave in ["m-77", "m-77", "m-31"]:
    nuevo = procesar(estado, clave)
    resultado = "procesada" if nuevo else "ignorada "
    # estado['cobros'] va entre comillas simples porque la f-string ya usa las dobles.
    print(f"clave {clave}: {resultado} cobros {estado['cobros']}")
