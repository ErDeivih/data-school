import time

# La division solo compensa si los subproblemas son mas baratos: comparamos tamanos.
def maximo_dyv(a):
    """Maximo por divide y venceras: partir hasta 1 elemento y combinar comparando."""
    if len(a) == 1:
        return a[0]
    medio = len(a) // 2
    return max(maximo_dyv(a[:medio]), maximo_dyv(a[medio:]))

def maximo_lineal(a):
    mejor = a[0]
    for v in a[1:]:
        if v > mejor:
            mejor = v
    return mejor

datos = list(range(1000, 0, -1))          # 1000 numeros, el maximo esta al principio
print("maximo dyv:   ", maximo_dyv(datos))       # -> maximo dyv:    1000
print("maximo lineal: ", maximo_lineal(datos))   # -> maximo lineal:  1000

inicio = time.perf_counter()
for _ in range(100):
    maximo_dyv(datos)
t_dyv = (time.perf_counter() - inicio) / 100

inicio = time.perf_counter()
for _ in range(100):
    maximo_lineal(datos)
t_lineal = (time.perf_counter() - inicio) / 100

print(f"dyv {t_dyv * 1e6:.1f} us  lineal {t_lineal * 1e6:.1f} us")
print("dyv es mas lento:", t_dyv > t_lineal)     # -> dyv es mas lento: True
