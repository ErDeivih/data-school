import inspect

def media_movil(serie, ventana):
    """Media movil simple.

    Args:
        serie: valores en orden temporal.
        ventana: numero de puntos que entran en cada media.

    Returns:
        Lista de medias; su longitud es len(serie) - ventana + 1.
    """
    return [sum(serie[i:i + ventana]) / ventana for i in range(len(serie) - ventana + 1)]

# La documentacion miente cuando alguien anade un argumento y no toca el docstring.
# Esta comprobacion cabe en un test y detecta justo eso.
firma = set(inspect.signature(media_movil).parameters)
documentados = {linea.strip().split(":")[0] for linea in inspect.getdoc(media_movil).splitlines()
                if linea.startswith("    ") and ":" in linea}

print("firma:        ", sorted(firma))
# -> firma:         ['serie', 'ventana']
print("docstring:    ", sorted(documentados))
# -> docstring:     ['serie', 'ventana']
print("sin documentar:", sorted(firma - documentados))
# -> sin documentar: []
print("resultado media_movil([1, 2, 3, 4], 2):", media_movil([1, 2, 3, 4], 2))
# -> resultado media_movil([1, 2, 3, 4], 2): [1.5, 2.5, 3.5]
