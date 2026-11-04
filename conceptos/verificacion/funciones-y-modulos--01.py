def interes_compuesto(capital, tasa, *, periodos=12):
    """Devuelve (capital final, interes ganado). El asterisco obliga a nombrar periodos."""
    factor = (1 + tasa / periodos) ** periodos
    return capital * factor, capital * (factor - 1)

final, ganado = interes_compuesto(1000, 0.06)
print("doce periodos:", round(final, 2), round(ganado, 2))        # -> 1061.68 61.68
print("cuatro periodos:", round(interes_compuesto(1000, 0.06, periodos=4)[0], 2))  # -> 1061.36

# return corta en seco: lo que venga despues no se ejecuta
def clasifica(x):
    if x < 0:
        return "negativo"
    return "positivo o cero"

print("clasifica:", clasifica(-3), clasifica(0))                 # -> negativo positivo o cero
