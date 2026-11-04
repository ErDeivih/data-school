import tracemalloc

# Para medir memoria hay que medirla, no adivinarla: cada objeto de Python tiene sobrecoste.
tracemalloc.start()
tabla = {}
for i in range(200_000):
    # El diccionario guarda 200.000 referencias AL MISMO objeto str, no 200.000 copias.
    tabla[i] = "x"                       # clave int, valor str
actual, pico = tracemalloc.get_traced_memory()   # pico = maximo alcanzado desde el start
tracemalloc.stop()

print("entradas:", len(tabla))                                # -> 200000
print(f"memoria actual {actual / 1024 / 1024:.1f} MiB")
print(f"pico {pico / 1024 / 1024:.1f} MiB")
# Dividir por el numero de entradas da el coste real de una entrada, metadatos incluidos.
print(f"sobrecoste por entrada {actual / len(tabla):.0f} bytes")
