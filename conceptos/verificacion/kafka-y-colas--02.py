# Reparto de particiones entre los miembros de un grupo y vigilancia del retraso.
n_particiones, n_consumidores = 6, 4
asignacion = {c: [] for c in range(n_consumidores)}
for p in range(n_particiones):
    asignacion[p % n_consumidores].append(p)

for consumidor, trozos in asignacion.items():
    print(f"consumidor {consumidor}: particiones {trozos}")

print("paralelismo maximo:", n_particiones)                       # -> paralelismo maximo: 6
print("consumidores sin particion con 8:", max(0, 8 - 6))         # -> consumidores sin particion con 8: 2

# Si el productor va mas rapido que el consumidor, el retraso crece sin freno.
lag = (1_000_000 - 200_000) * 5
print("retraso tras 5 horas:", lag)                               # -> retraso tras 5 horas: 4000000
