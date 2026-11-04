def f(x):
    return (x ** 2 - 1) / (x - 1)

# En x = 1 hay 0/0: la funcion no esta definida, pero los valores se acercan a 2.
print("f(0.9) :", round(f(0.9), 3))     # -> 1.9
print("f(0.99):", round(f(0.99), 3))    # -> 1.99
print("f(1.01):", round(f(1.01), 3))    # -> 2.01
print("f(1.1) :", round(f(1.1), 3))     # -> 2.1

# La funcion signo: los laterales existen pero no coinciden, asi que no hay limite.
def g(x):
    return -1.0 if x < 0 else (0.0 if x == 0 else 1.0)

print("lateral izquierdo:", g(-0.001))   # -> -1.0
print("lateral derecho  :", g(0.001))    # -> 1.0
print("valor en el punto:", g(0.0))      # -> 0.0
