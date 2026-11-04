# f es continua y cambia de signo en [1, 2]: Bolzano garantiza una raiz dentro.
def f(x):
    return x ** 3 - x - 2

print("f(1):", f(1.0))   # -> -2.0
print("f(2):", f(2.0))   # -> 4.0

lo, hi = 1.0, 2.0
for _ in range(60):
    mid = (lo + hi) / 2
    if f(mid) < 0:
        lo = mid
    else:
        hi = mid
print("raiz aproximada:", round((lo + hi) / 2, 6))   # -> 1.52138
