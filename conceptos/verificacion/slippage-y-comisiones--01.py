# Los tres costes y la ventaja neta, en puntos basicos sobre el nominal.
comision_pb = 4.0        # por punta: se paga al entrar y al salir
diferencial_pb = 4.0     # cruzar a mercado una vez por vuelta
impacto_pb = 1.0
ventaja_bruta_pb = 15.0

coste_pb = 2 * comision_pb + diferencial_pb + impacto_pb
neta_pb = ventaja_bruta_pb - coste_pb

print("coste ida y vuelta:", round(coste_pb, 1), "pb")     # -> 13.0 pb
print("ventaja neta      :", round(neta_pb, 1), "pb")      # -> 2.0 pb

nominal = 25_000
print("coste en euros    :", round(nominal * coste_pb / 10_000, 2))    # -> 32.5
print("neto en euros     :", round(nominal * neta_pb / 10_000, 2))      # -> 5.0

# La ventaja bruta minima para no perder con estos costes.
print("ventaja de equilibrio:", round(coste_pb, 1), "pb")  # -> 13.0 pb
