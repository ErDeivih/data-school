from datetime import datetime

# Hitos del incidente: se reconstruyen DESPUES, a partir de alertas y registros.
def t(hhmm):
    return datetime.strptime("2026-03-14 " + hhmm, "%Y-%m-%d %H:%M")

inicio, deteccion, mitigacion, restauracion = t("03:02"), t("03:05"), t("03:40"), t("04:10")

def minutos(a, b):
    # total_seconds() es un float con los segundos enteros y los microsegundos aparte: aqui no
    # hay microsegundos, pero dividir y convertir a int evita imprimir "65.0" mas adelante.
    return int((b - a).total_seconds() / 60)

print("MTTD  minutos:", minutos(inicio, deteccion))       # -> 3
print("MTTM  minutos:", minutos(deteccion, mitigacion))   # -> 35
print("MTTR  minutos:", minutos(deteccion, restauracion)) # -> 65
print("impacto usuarios:", minutos(inicio, restauracion), "minutos")  # -> 68
