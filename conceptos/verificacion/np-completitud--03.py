import time

# La verificacion no crece con el problema; la busqueda si. Mismo problema, dos costes.
def verificar_subconjunto(numeros, objetivo, elegidos):
    return sum(numeros[i] for i in elegidos) == objetivo

def contar_subconjuntos_posibles(n):
    return 2 ** n

for n in (10, 20, 30):
    print(f"n={n:>2}  combinaciones={contar_subconjuntos_posibles(n):>12,}  "
          f"sumas para verificar={n:>3}")
# -> n=10  combinaciones=       1,024  sumas para verificar= 10
# -> n=20  combinaciones=   1,048,576  sumas para verificar= 20
# -> n=30  combinaciones=1,073,741,824  sumas para verificar= 30

inicio = time.perf_counter()
comprobado = verificar_subconjunto(list(range(30)), 15, [0, 1, 2, 3, 4, 5])
micros = (time.perf_counter() - inicio) * 1e6
print("verificacion de 6 indices:", comprobado, f"en {micros:.1f} us")
print("es polinomica:", micros < 1000)       # -> es polinomica: True
