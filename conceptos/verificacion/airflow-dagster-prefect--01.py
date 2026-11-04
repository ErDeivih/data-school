from datetime import datetime, timedelta

# La fecha logica marca el INICIO del intervalo de datos, no el dia del disparo.
inicio_dag = datetime(2024, 3, 1, 3, 0)      # start_date de la programacion "0 3 * * *"

for desplazamiento in (0, 12, 13):
    logical_date = inicio_dag + timedelta(days=desplazamiento)
    fin_intervalo = logical_date + timedelta(days=1)
    print(f"logical_date {logical_date:%m-%d %H:%M} cubre "
          f"[{logical_date:%m-%d %H:%M}, {fin_intervalo:%m-%d %H:%M}) "
          f"y se dispara el {fin_intervalo:%m-%d %H:%M}")

desde, hasta = datetime(2024, 3, 8, 3, 0), datetime(2024, 3, 15, 3, 0)
print("ejecuciones del reproceso 8-14 de marzo:", (hasta - desde).days)   # -> ejecuciones del reproceso 8-14 de marzo: 7
