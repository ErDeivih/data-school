# El embudo de calidad de las tres capas, con los numeros del ejemplo.
crudas = 1_000_000
duplicadas = 3_000            # repeticiones exactas de la ingesta
sin_importe = 12_000          # filas que llegaron sin importe

plata = crudas - duplicadas
validas = plata - sin_importe
importe_medio = 5.00

print(f"bronce  {crudas:>10,} filas")
print(f"plata   {plata:>10,} filas   (-{duplicadas / crudas:.1%} duplicadas)")
print(f"validas {validas:>10,} filas   (-{sin_importe / crudas:.1%} sin importe)")
print(f"oro: facturado {validas * importe_medio:>12,.2f} EUR")
