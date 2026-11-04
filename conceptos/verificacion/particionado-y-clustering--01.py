# Tabla de 4 TB con 4 anos de 365 dias: cuanto se lee con y sin poda
tam_tabla_gb = 4096
dias = 4 * 365
tam_particion_gb = tam_tabla_gb / dias

print("particiones por fecha:", dias)                        # -> particiones por fecha: 1460
print("GB por particion:", round(tam_particion_gb, 2))       # -> GB por particion: 2.81
print("porcentaje leido en un dia:", round(100 / dias, 4))   # -> porcentaje leido en un dia: 0.0685

precio_tb = 5.0    # precio hipotetico por TB escaneado
print("coste sin podar:", round(tam_tabla_gb / 1024 * precio_tb, 2), "USD")    # -> coste sin podar: 20.0 USD
print("coste podando:", round(tam_particion_gb / 1024 * precio_tb, 3), "USD")  # -> coste podando: 0.014 USD
