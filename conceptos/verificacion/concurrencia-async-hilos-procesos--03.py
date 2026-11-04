import os
import time
from concurrent.futures import ProcessPoolExecutor

def carga_cpu(n):
    total = 0
    for i in range(n):
        total += (i * i) % 997          # bucle de Python puro: aqui el GIL no deja solapar nada
    return total

if __name__ == "__main__":              # obligatorio en Windows: los hijos reimportan el modulo
    TRABAJOS = [1_000_000] * 4          # cuatro tareas identicas, una por nucleo

    inicio = time.perf_counter()
    # map devuelve un iterador perezoso: sin list() no se ejecutaria nada y el tiempo saldria 0
    list(map(carga_cpu, TRABAJOS))
    t_serie = time.perf_counter() - inicio

    inicio = time.perf_counter()
    # max_workers reparte las tareas entre procesos; el pool se cierra solo al salir del with
    with ProcessPoolExecutor(max_workers=4) as pool:
        # los resultados vuelven en el mismo orden en que se enviaron, no en el de llegada
        resultados = list(pool.map(carga_cpu, TRABAJOS))
    t_procesos = time.perf_counter() - inicio

    print("nucleos disponibles:", os.cpu_count())
    print("resultados:")
    for r in resultados:
        print("  ", r)
    print(f"en serie    {t_serie * 1000:7.0f} ms")
    print(f"4 procesos  {t_procesos * 1000:7.0f} ms")
    print("cada proceso arranca de cero: el modulo se reimporta y los datos se copian")
