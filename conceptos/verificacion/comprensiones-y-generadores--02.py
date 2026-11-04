# yield convierte la funcion en una fabrica de valores perezosa
def cuenta_atras(desde):
    print("empieza el generador")
    while desde > 0:
        yield desde
        desde -= 1
    print("se acabo")

generador = cuenta_atras(3)
print("creado, sin ejecutar nada")     # -> creado, sin ejecutar nada: nada se ha impreso del generador
print("primero:", next(generador))     # -> empieza el generador
                                       # -> primero: 3
print("resto:", list(generador))       # -> se acabo
                                       # -> resto: [2, 1]
