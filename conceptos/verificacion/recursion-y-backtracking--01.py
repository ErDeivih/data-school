import sys

def fib_llamadas(n, contador):
    contador[0] += 1
    if n < 2:
        return n
    return fib_llamadas(n - 1, contador) + fib_llamadas(n - 2, contador)

for n in (10, 20, 30):
    contador = [0]
    valor = fib_llamadas(n, contador)
    print(f"fib({n:>2}) = {valor:>8}  llamadas = {contador[0]:>9}")

# La pila de llamadas es finita: pasarse de profundidad es un error, no una lentitud.
print("limite de recursion:", sys.getrecursionlimit())   # -> limite de recursion: 1000
try:
    fib_llamadas(2000, [0])
except RecursionError:
    print("RecursionError a profundidad 2000")          # -> RecursionError a profundidad 2000
