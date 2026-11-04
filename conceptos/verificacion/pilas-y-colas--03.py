from collections import deque

# Sacar por delante: contamos desplazamientos en vez de cronometrar.
def desplazamientos_con_lista(cola):
    total = 0
    while cola:
        cola.pop(0)              # saca el primero y mueve todos los demas
        total += len(cola)       # lo que se ha desplazado en esa operacion
    return total

def desplazamientos_con_deque(cola):
    total = 0
    while cola:
        cola.popleft()           # no desplaza nada: actualiza un puntero
        total += 1
    return total

print("lista, 10000 elementos:", desplazamientos_con_lista(list(range(10000))))   # -> lista, 10000 elementos: 49995000
print("deque, 10000 elementos:", desplazamientos_con_deque(deque(range(10000))))  # -> deque, 10000 elementos: 10000
