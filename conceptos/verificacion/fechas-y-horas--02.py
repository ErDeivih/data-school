import datetime as dt
from zoneinfo import ZoneInfo

madrid = ZoneInfo("Europe/Madrid")
utc = dt.timezone.utc

instante = dt.datetime(2026, 7, 15, 6, 0, tzinfo=utc)      # un punto del tiempo
en_madrid = instante.astimezone(madrid)                    # el mismo punto, otro reloj
print("UTC:   ", instante.strftime("%Y-%m-%d %H:%M %Z"))   # -> 2026-07-15 06:00 UTC
print("Madrid:", en_madrid.strftime("%Y-%m-%d %H:%M %Z"))  # -> 2026-07-15 08:00 CEST
print("desfase de Madrid en julio:", en_madrid.utcoffset())  # -> 2:00:00

medianoche = dt.datetime(2026, 3, 29, tzinfo=madrid)       # dia del cambio de hora
dia_siguiente = medianoche + dt.timedelta(days=1)          # +1 dia de calendario
print("horas reales del 29 de marzo:",
      dia_siguiente.astimezone(utc) - medianoche.astimezone(utc))          # -> 23:00:00
print("mismo instante con dos nombres:", medianoche == medianoche.astimezone(utc))  # -> True
