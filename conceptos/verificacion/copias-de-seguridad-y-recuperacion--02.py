# Cuatro copias no valen cuatro veces mas: valen la probabilidad de que fallen a la vez.
p_copia_inservible = 0.01
for n in (1, 2, 3, 4):
    print("%d copia(s) -> probabilidad de perderlo todo: %.0e" % (n, p_copia_inservible ** n))
# -> 1 copia(s) -> probabilidad de perderlo todo: 1e-02
# -> 3 copia(s) -> probabilidad de perderlo todo: 1e-06

# El coste esperado decide cuanto se gasta en el plan: frecuencia por dano por incidente.
coste_hora_paron = 12000
rto_horas = 2.5
valor_pedido = 40
for frecuencia in (1.0, 0.2, 0.05):        # incidentes graves al ano
    for pedidos_perdidos in (3000, 10):
        dano = rto_horas * coste_hora_paron + pedidos_perdidos * valor_pedido
        print("%.2f incidentes/ano, %5d pedidos perdidos -> %.0f EUR/ano"
              % (frecuencia, pedidos_perdidos, frecuencia * dano))
# -> 0.20 incidentes/ano,  3000 pedidos perdidos -> 30000 EUR/ano
# -> 0.20 incidentes/ano,    10 pedidos perdidos -> 6080 EUR/ano
