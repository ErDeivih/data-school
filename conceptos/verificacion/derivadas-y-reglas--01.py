def f(x):
    return 3 * x ** 2 - 2 * x + 1

def pendiente_numerica(x, h):
    return (f(x + h) - f(x)) / h

# Al reducir h, el cociente incremental se acerca a la derivada exacta, que vale 10.
print("h=0.1   :", round(pendiente_numerica(2, 0.1), 4))     # -> 10.3
print("h=0.01  :", round(pendiente_numerica(2, 0.01), 4))    # -> 10.03
print("h=0.001 :", round(pendiente_numerica(2, 0.001), 4))   # -> 10.003
print("exacta  :", 6 * 2 - 2)                                # -> 10

# Con h demasiado pequeno la resta pierde precision y la aproximacion empeora.
print("h=1e-13 :", round(pendiente_numerica(2, 1e-13), 6))   # -> 9.983125
