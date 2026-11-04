# Plan de transicion: horas por hito repartidas al ritmo semanal que puedes sostener.
hitos = {
    "experimento_ab": 30,
    "modelo_con_validacion_temporal": 45,
    "informe_defendido": 20,
    "sql_ventanas": 25,
}
horas_semana = 6
total = sum(hitos.values())

print(f"total {total} h -> {total / horas_semana:.0f} semanas a {horas_semana} h/semana")
# Ordenados por coste: lo que mas tarda es lo que hay que empezar antes.
for nombre, horas in sorted(hitos.items(), key=lambda par: -par[1]):
    print(f"{nombre:32s} {horas:3d} h  {horas / horas_semana:.1f} semanas")
