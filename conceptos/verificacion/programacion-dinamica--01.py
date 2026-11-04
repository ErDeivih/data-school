from functools import lru_cache

# Version con memoizacion: se escribe la recursion natural y se envuelve.
@lru_cache(maxsize=None)
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)

# Version con tabulacion: se rellena de abajo arriba, sin recursion.
def fib_tabla(n):
    a, b = 0, 1                    # F(0) y F(1)
    for _ in range(n):
        a, b = b, a + b
    return a

print("fib_memo(30):", fib_memo(30))                  # -> fib_memo(30): 832040
print("fib_tabla(30):", fib_tabla(30))                # -> fib_tabla(30): 832040
print("llamadas distintas:", fib_memo.cache_info().currsize)   # -> llamadas distintas: 31
print("aciertos en cache:", fib_memo.cache_info().hits)       # -> aciertos en cache: 28
