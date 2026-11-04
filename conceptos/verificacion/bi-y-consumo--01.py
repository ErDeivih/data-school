# Coste mensual de servir el mismo cuadro de las dos maneras.
consultas_mes = 6000
gb_por_consulta = 2.0      # lo que escanea una consulta sin podar la particion
gb_tabla = 60.0            # lo que ocupa la tabla que copia el extracto
refrescos_mes = 30
precio_tb = 5.0            # tarifa de ejemplo: euros por TB escaneado
gb_por_tb = 1000.0

viva = consultas_mes * gb_por_consulta / gb_por_tb * precio_tb
extracto = refrescos_mes * gb_tabla / gb_por_tb * precio_tb
# Cruce: consultas al mes que igualan el coste del extracto (aqui se cancela precio_tb)
cruce = refrescos_mes * gb_tabla / gb_por_consulta

print(f"consulta viva {viva:7.2f} EUR/mes")             # -> 60.00
print(f"extracto      {extracto:7.2f} EUR/mes")         # -> 9.00
print(f"cruce en {cruce:.0f} consultas/mes")            # -> 900
