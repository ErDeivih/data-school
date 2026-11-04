# Cuanto mejora el peor caso con salting, y cuanto cuesta la replica del lado pequeno.
filas = 120_000_000
caliente = 48_000_000          # una sola clave concentra el 40 % de las filas
particiones = 400
resto_por_tarea = (filas - caliente) / particiones

peor_sin = caliente + resto_por_tarea
media = filas / particiones
print(f"tarea media             {media:>12,.0f} filas")
print(f"peor tarea sin salting  {peor_sin:>12,.0f} filas")
print(f"factor de desequilibrio {peor_sin / media:>12.1f}x")

trozos = 64
peor_con = caliente / trozos + resto_por_tarea
print(f"peor tarea con salting  {peor_con:>12,.0f} filas")
print(f"mejora del peor caso    {peor_sin / peor_con:>12.1f}x")

mb_dimension = 20
print(f"replica del lado pequeno {mb_dimension * trozos:>11,} MB")
