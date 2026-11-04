# Espera en la cola FIFO: no es solo cuestion de latencia de red
delante = 3000            # acciones por delante de tu orden, a tu mismo precio

for flujo in (300, 900, 3000):
    print(f"flujo {flujo:>5} acciones/min -> espera {delante / flujo:>4.1f} min")
# -> flujo   300 acciones/min -> espera 10.0 min
# -> flujo   900 acciones/min -> espera  3.3 min
# -> flujo  3000 acciones/min -> espera  1.0 min
