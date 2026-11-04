# La condicion de utilizacion: por que el equipo central no escala con la demanda.
dominios = 40
peticiones_por_dominio = 2
demanda = dominios * peticiones_por_dominio

horas_utiles_mes = 120
horas_por_peticion = 12

for personas in (3, 6, 12):
    capacidad = personas * horas_utiles_mes / horas_por_peticion
    print(f"{personas:>2} personas -> capacidad {capacidad:>4.0f}, utilizacion {demanda / capacidad:>5.0%}")
