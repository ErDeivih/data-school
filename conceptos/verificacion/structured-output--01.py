# Validador minimo: sin librerias, para que se vea que comprobar es barato.
ESQUEMA = {
    # el tipo se declara con la CLASE (str, float), no con su nombre entre comillas
    "concepto": {"tipo": str, "requerido": True, "long_min": 1, "long_max": 80},
    "importe": {"tipo": float, "requerido": True, "minimo": 0.0},
    "moneda": {"tipo": str, "requerido": True, "enum": ["EUR", "USD", "GBP"]},   # enum: lista cerrada
    "notas": {"tipo": str, "requerido": False},     # False explicito: este campo puede faltar
}

def validar(dato, esquema=ESQUEMA):
    errores = []
    for campo, regla in esquema.items():        # recorre el ESQUEMA: busca lo que falta y lo que esta mal
        if campo not in dato:
            # .get devuelve None si la clave no existe, y None es falso: sin "requerido" el campo es opcional
            if regla.get("requerido"):
                errores.append((campo, "falta un campo obligatorio"))
            continue                            # sin valor no hay nada mas que comprobar en este campo
        valor = dato[campo]
        if not isinstance(valor, regla["tipo"]):
            # __name__ da el nombre de la clase para el mensaje: "float", no <class 'float'>
            errores.append((campo, "se esperaba " + regla["tipo"].__name__))
        elif "enum" in regla and valor not in regla["enum"]:
            # los elif encadenados: este solo se comprueba si el tipo ya era correcto
            errores.append((campo, "valor fuera de la lista permitida"))
        elif "minimo" in regla and valor < regla["minimo"]:
            errores.append((campo, "valor por debajo del minimo"))
        elif "long_min" in regla and len(valor) < regla["long_min"]:
            # len() aqui es seguro porque el tipo str ya se ha comprobado antes
            errores.append((campo, "texto demasiado corto"))
    for campo in dato:                          # recorre la RESPUESTA: caza los campos que sobran
        if campo not in esquema:
            errores.append((campo, "campo desconocido"))
    return errores                              # lista de tuplas (campo, motivo); vacia = respuesta valida

respuestas = [
    {"concepto": "Licencia anual", "importe": 1250.0, "moneda": "EUR"},
    {"concepto": "Licencia anual", "importe": "1250,00", "moneda": "EUR"},
    {"concepto": "Licencia anual", "importe": -10.0, "moneda": "euros"},
]

for r in respuestas:
    errores = validar(r)
    print(("valida  " if not errores else "rechaza ") + str(errores))
# valida  []
# rechaza [('importe', 'se esperaba float')]
# rechaza [('importe', 'valor por debajo del minimo'), ('moneda', 'valor fuera de la lista permitida')]
