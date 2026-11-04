# Cuanto empeora el resultado al operar mas grande: el impacto no es lineal.
def impacto_pb(tamano, tamano_base=25_000, impacto_base=1.0):
    """Modelo de raiz cuadrada: el impacto crece con la raiz del tamano relativo."""
    return impacto_base * (tamano / tamano_base) ** 0.5

for tamano in (25_000, 100_000, 250_000, 1_000_000):
    coste = 2 * 4.0 + 4.0 + impacto_pb(tamano)
    print(f"nominal {tamano:>9,}  impacto {impacto_pb(tamano):5.2f} pb  coste {coste:5.2f} pb")
# -> nominal    25,000  impacto  1.00 pb  coste 13.00 pb
# -> nominal   100,000  impacto  2.00 pb  coste 14.00 pb
# -> nominal   250,000  impacto  3.16 pb  coste 15.16 pb
# -> nominal 1,000,000  impacto  6.32 pb  coste 18.32 pb
