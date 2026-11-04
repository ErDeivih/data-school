def leer_importe(texto):
    try:
        return float(texto)
    except ValueError as error:
        # raise ... from conserva la causa: el traceback muestra las dos
        raise ValueError("importe no numerico: " + texto) from error

try:
    leer_importe("doce")
except ValueError as error:
    print("mensaje:", error)                                  # -> mensaje: importe no numerico: doce
    print("causa:", type(error.__cause__).__name__)           # -> causa: ValueError

# assert documenta un supuesto del programador: si es falso, avisa en vez de seguir
def ratio(a, b):
    assert b != 0, "el denominador no puede ser cero"
    return a / b

print("ratio:", ratio(6, 3))                                  # -> ratio: 2.0
try:
    ratio(6, 0)
except AssertionError as error:
    print("assert:", error)                                   # -> assert: el denominador no puede ser cero
