# Antes de pegar codigo, tres preguntas de defensa: ¿y si la lista esta vacia?, ¿y si
# falta un dato?, ¿y si llega un texto? Lo que no sepas contestar, no lo pegues.
def ticket_medio(importes):
    return sum(importes) / len(importes)

casos = {
    "tres importes": [10.0, 20.0, 30.0],
    "un nulo":       [10.0, None, 30.0],
    "sin ventas":    [],
}
for nombre, datos in casos.items():
    try:
        print(f"{nombre:14s} -> {ticket_medio(datos)}")
    except Exception as error:
        print(f"{nombre:14s} -> {type(error).__name__}: {error}")
# -> tres importes -> 20.0
# -> un nulo       -> TypeError: unsupported operand type(s) for +: 'float' and 'NoneType'
# -> sin ventas    -> ZeroDivisionError: division by zero
