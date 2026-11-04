# Cuanto aguanta una posicion corta antes de que el alquiler se coma la ventaja
precio = 50.0
acciones = 100
ventaja_diaria = 0.02      # EUR por accion y dia que aporta la tesis

for alquiler, rebate in ((0.03, 0.01), (0.12, 0.01), (0.40, 0.0)):
    coste_dia = (alquiler - rebate) * precio / 365
    neto_dia = ventaja_diaria - coste_dia
    dias = ventaja_diaria / coste_dia if coste_dia > 0 else float("inf")
    print(f"alquiler {alquiler:>4.0%}, rebate {rebate:>4.0%}: coste {coste_dia:.5f} EUR/accion/dia, "
          f"neto {neto_dia * acciones:+.2f} EUR/dia, techo {dias:.1f} dias")
# -> alquiler  3%, rebate  1%: coste 0.00274 EUR/accion/dia, neto +1.73 EUR/dia, techo 7.3 dias
# -> alquiler 12%, rebate  1%: coste 0.01507 EUR/accion/dia, neto +0.49 EUR/dia, techo 1.3 dias
# -> alquiler 40%, rebate  0%: coste 0.05479 EUR/accion/dia, neto -3.48 EUR/dia, techo 0.4 dias
