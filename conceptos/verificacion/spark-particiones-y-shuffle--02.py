# El tamano de particion manda: la misma tarea, con tres configuraciones distintas.
shuffle_gb = 20
for p in (8, 200, 10_000):
    mb = shuffle_gb * 1024 / p
    print(f"{p:>6} particiones -> {mb:>10,.1f} MB por tarea")
