import asyncio
import time

async def descarga(nombre, segundos):
    # sleep de asyncio, NO time.sleep: cede el control al bucle y deja correr las demas tareas
    await asyncio.sleep(segundos)      # simula la espera de red, sin bloquear
    return f"{nombre} listo"

async def secuencial():
    inicio = time.perf_counter()               # reloj de pared: lo que espera una persona
    for nombre, segundos in [("a", 0.30), ("b", 0.20), ("c", 0.10)]:
        await descarga(nombre, segundos)       # una detras de otra: aqui si se espera cada una
    return time.perf_counter() - inicio

async def en_paralelo():
    inicio = time.perf_counter()
    # gather lanza las tres corrutinas y devuelve una lista con los resultados EN EL ORDEN
    # en que se pasaron, no en el orden en que terminan; tarda lo que la mas lenta.
    await asyncio.gather(descarga("a", 0.30), descarga("b", 0.20), descarga("c", 0.10))
    return time.perf_counter() - inicio

t_sec = asyncio.run(secuencial())      # asyncio.run arranca el bucle, ejecuta y lo cierra
t_par = asyncio.run(en_paralelo())     # dos run seguidos: un bucle nuevo para cada uno
print(f"una tras otra {t_sec:.2f} s")     # -> 0.60 s (suma de las esperas)
print(f"con gather    {t_par:.2f} s")     # -> 0.30 s (la mas lenta)
print("aceleracion:", round(t_sec / t_par, 1), "x")
