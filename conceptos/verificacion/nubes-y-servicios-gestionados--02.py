# Presupuesto antes de gastar: cuanto va a leer de verdad una consulta.
# Los almacenes que cobran por bytes escaneados hacen que esto sea dinero, no curiosidad.
bytes_totales = 4 * 1024 ** 3       # 4 GB de tabla, 4 anos de historia
dias = 4 * 365
bytes_del_mes = bytes_totales / dias * 31
print(f"tabla entera      {bytes_totales / 1024**3:.1f} GB")                    # -> 4.0 GB
print(f"un mes si esta particionada por fecha  {bytes_del_mes / 1024**3:.3f} GB")  # -> 0.085 GB
print(f"la misma consulta sin particionar cuesta ~{bytes_totales / bytes_del_mes:.0f} veces mas")
# -> la misma consulta sin particionar cuesta ~47 veces mas
