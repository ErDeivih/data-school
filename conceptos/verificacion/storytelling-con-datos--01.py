import math

# Conversiones en dos periodos de 400 visitas cada uno.
visitas, antes, despues = 400, 13, 14
tasa_antes, tasa_despues = antes / visitas, despues / visitas

# Error tipico de una diferencia de proporciones con muestras del mismo tamano.
p = (antes + despues) / (2 * visitas)
error = math.sqrt(p * (1 - p) * (2 / visitas))

print(f"tasa antes {tasa_antes:.1%}  tasa despues {tasa_despues:.1%}")
print(f"cambio relativo {(tasa_despues - tasa_antes) / tasa_antes:+.1%}")
print(f"diferencia observada {despues - antes} conversion, error tipico {error:.2%}")
print("cambio creible:", abs(tasa_despues - tasa_antes) > 2 * error)
