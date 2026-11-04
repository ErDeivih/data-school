from datetime import datetime

# Por que el lote atribuye mal los eventos que llegan tarde: el corte es una frontera dura.
corte = datetime(2024, 3, 1, 10, 0)          # el lote de las 10:00 cierra a las 10:00 en punto
ocurridos = [datetime(2024, 3, 1, 9, 58), datetime(2024, 3, 1, 9, 59), datetime(2024, 3, 1, 9, 55)]
llegadas = [datetime(2024, 3, 1, 9, 59, 10), datetime(2024, 3, 1, 9, 59, 40), datetime(2024, 3, 1, 10, 3)]

en_el_lote = sum(1 for t in llegadas if t < corte)
print("eventos en el lote de las 10:00:", en_el_lote)                    # -> eventos en el lote de las 10:00: 2
print("eventos que van al lote siguiente:", len(llegadas) - en_el_lote)  # -> eventos que van al lote siguiente: 1

# El tercero ocurrio a las 9:55, pero llegara a las 10:03 y se contara en la hora siguiente.
retraso = (llegadas[2] - ocurridos[2]).total_seconds()
print("retraso en segundos:", int(retraso))                              # -> retraso en segundos: 480
