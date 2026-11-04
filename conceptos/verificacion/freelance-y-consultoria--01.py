# Tarifa minima: los dias que de verdad puedes facturar no son los laborables.
dias_laborables = 220        # laborables netos: sin festivos ni vacaciones
dias_no_facturables = 55     # formacion, propuestas, administracion, comercial
horas_dia = 7.5              # de 8 horas, media se va en correo y reuniones internas
horas_facturables = (dias_laborables - dias_no_facturables) * horas_dia
objetivo_neto = 45000        # lo que quieres llevarte antes de impuestos
costes_fijos = 12000         # cuota, gestoria, seguros, software, equipo
tarifa = (objetivo_neto + costes_fijos) / horas_facturables

print(f"dias facturables   {dias_laborables - dias_no_facturables}")  # -> 165
print(f"horas facturables  {horas_facturables:.0f}")                 # -> 1238
print(f"tarifa minima      {tarifa:.2f} EUR/h")                      # -> 46.06 EUR/h
