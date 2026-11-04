# Un informe no acaba en la metrica: acaba en la decision. Matriz de confusion de un
# modelo de impago sobre 1.000 solicitudes (100 impagan y 900 pagan), a dos umbrales.
coste_impago = 4000.0   # EUR que se pierden si se concede y no paga
margen_bueno = 300.0    # EUR que se dejan de ganar si se rechaza a quien si pagaba

def coste(impagos_concedidos, buenos_rechazados):
    return impagos_concedidos * coste_impago + buenos_rechazados * margen_bueno

for umbral, impagos, buenos in [("0.50", 40, 45), ("0.30", 15, 120)]:
    print(f"umbral {umbral}: {impagos} impagos concedidos, {buenos} buenos rechazados, "
          f"coste {coste(impagos, buenos):,.0f} EUR por 1.000 solicitudes")
# -> umbral 0.50: 40 impagos concedidos, 45 buenos rechazados, coste 173,500 EUR por 1.000 solicitudes
# -> umbral 0.30: 15 impagos concedidos, 120 buenos rechazados, coste 96,000 EUR por 1.000 solicitudes

print(f"ahorro al bajar el umbral: {coste(40, 45) - coste(15, 120):,.0f} EUR")
# -> ahorro al bajar el umbral: 77,500 EUR
