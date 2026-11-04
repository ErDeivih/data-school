# Profundidad de la pila: cuantas funciones hay que atravesar hasta el fallo
def tercer_nivel(n):
    return 10 / n

def segundo_nivel(n):
    return tercer_nivel(n)

def primer_nivel(n):
    return segundo_nivel(n)

try:
    primer_nivel(0)
except ZeroDivisionError as error:
    import traceback
    profundidad = len(traceback.extract_tb(error.__traceback__))
    print("funciones en la pila:", profundidad)     # -> funciones en la pila: 4
    print("ultima funcion:", traceback.extract_tb(error.__traceback__)[-1].name)  # -> tercer_nivel
