import datetime as dt

inicio = dt.datetime(2026, 3, 1, 9, 0)      # datetime "ingenuo": no dice de que zona es
fin = inicio + dt.timedelta(days=10, hours=4, minutes=30)
print("fin:", fin)                                            # -> 2026-03-11 13:30:00
print("duracion:", fin - inicio)                              # -> 10 days, 4:30:00
print("fecha suelta:", fin.date(), " hora suelta:", fin.time())  # -> 2026-03-11 y 13:30:00
print("formateado:", fin.strftime("%d/%m/%Y %H:%M"))          # -> 11/03/2026 13:30
print("dias hasta el 20 de marzo:", (dt.datetime(2026, 3, 20) - fin).days)   # -> 8
