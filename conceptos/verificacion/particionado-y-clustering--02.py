# Elegir la granularidad: el objetivo esta entre 128 MB y 1 GB por particion
tam_tabla_mb = 4096 * 1024

print("solo por fecha:", round(tam_tabla_mb / 1460, 1), "MB por particion")              # -> solo por fecha: 2872.8 MB por particion
print("por fecha y hora:", round(tam_tabla_mb / (1460 * 24), 1), "MB por particion")     # -> por fecha y hora: 119.7 MB por particion
print("por fecha y cliente:", round(tam_tabla_mb / (1460 * 5000), 2), "MB por particion")  # -> por fecha y cliente: 0.57 MB por particion
print("ficheros con fecha y cliente:", 1460 * 5000)                                      # -> ficheros con fecha y cliente: 7300000
