import traceback

def precio_medio(importes, noches):
    return sum(importes) / noches

try:
    precio_medio([100, 150], 0)
except ZeroDivisionError as error:
    lineas = traceback.format_exc().splitlines()
    print("tipo:", type(error).__name__)                    # -> tipo: ZeroDivisionError
    print("mensaje:", error)                                # -> mensaje: division by zero
    print("ultima linea:", lineas[-1].strip())              # -> ultima linea: ZeroDivisionError: division by zero
