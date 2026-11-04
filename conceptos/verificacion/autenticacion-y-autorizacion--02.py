# Matriz de permisos: que roles pueden hacer cada accion.
PERMISOS = {
    "ver":    {"lector", "editor", "admin"},     # conjuntos: la pertenencia es inmediata
    "editar": {"editor", "admin"},
    "borrar": {"admin"},
}

def autorizar(rol, accion):
    if rol is None:                              # is None, no == None: es el valor ausente
        return 401, "no se quien eres"
    if rol not in PERMISOS[accion]:
        # PERMISOS[accion] lanza KeyError si la accion no existe; en un servicio real, 404 o 405
        return 403, "se quien eres, pero no puedes"
    return 200, "adelante"                       # devuelve una tupla (codigo, motivo)

casos = [(None, "ver"), ("lector", "ver"), ("lector", "borrar"), ("admin", "borrar")]
for rol, accion in casos:
    estado, motivo = autorizar(rol, accion)      # desempaqueta la tupla que devuelve la funcion
    print(f"rol={str(rol):<7} accion={accion:<7} -> {estado} {motivo}")
    # :<7 alinea a la izquierda en 7 caracteres para que las columnas cuadren; str(None) es "None"
