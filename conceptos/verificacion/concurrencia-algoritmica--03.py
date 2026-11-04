import threading

# Con un candado, leer-modificar-escribir se vuelve una sola operacion para los demas.
CONTADOR = [0]
candado = threading.Lock()
POR_HILO = 50_000
N_HILOS = 4

def sumar(n):
    for _ in range(n):
        with candado:
            CONTADOR[0] += 1

hilos = [threading.Thread(target=sumar, args=(POR_HILO,)) for _ in range(N_HILOS)]
for h in hilos:
    h.start()
for h in hilos:
    h.join()

print("esperado:", N_HILOS * POR_HILO)                        # -> 200000
print("obtenido:", CONTADOR[0])                               # -> 200000
print("coincide:", CONTADOR[0] == N_HILOS * POR_HILO)         # -> True
