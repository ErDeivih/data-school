# Aritmetica del ahorro: con tarifas redondas supuestas, lo que importa es la forma.
gb_particion = 8
particiones = 24
meses_consultados = 3
ejecuciones_mes = 30
tarifa_gb = 0.005        # unidades monetarias por GB leido (tarifa supuesta)

gb_antes = gb_particion * particiones * ejecuciones_mes
gb_despues = gb_particion * meses_consultados * ejecuciones_mes

print("GB al mes barriendo todo:  ", gb_antes)          # -> 5760
print("GB al mes leyendo 3 de 24:", gb_despues)         # -> 720
print("factor de reduccion:      ", gb_antes / gb_despues)   # -> 8.0
print("ahorro mensual:", round((gb_antes - gb_despues) * tarifa_gb, 2))  # -> 25.2
