import pandas as pd

# El calendario: no todos los dias naturales tienen precio.
dias = pd.date_range("2024-07-01", "2024-07-07", freq="D")
print(len(dias))                                     # -> 7
print(dias.day_name().tolist())
# -> ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

laborables = pd.bdate_range("2024-07-01", "2024-07-07")
print(len(laborables))                               # -> 5

# La sesion se ancla a la plaza, no al portatil: la misma apertura en tres relojes.
apertura = pd.Timestamp("2024-07-01 09:30", tz="America/New_York")
print(apertura.tz_convert("UTC").strftime("%H:%M"))        # -> 13:30
print(apertura.tz_convert("Europe/Madrid").strftime("%H:%M"))  # -> 15:30

# El 27 de octubre de 2024 las 02:30 en Madrid existen DOS veces: hay que decidir cual.
ambiguas = pd.Series(pd.to_datetime(["2024-10-27 02:30"]))
print(ambiguas.dt.tz_localize("Europe/Madrid", ambiguous=True)[0].strftime("%H:%M %z"))
# -> 02:30 +0200
print(ambiguas.dt.tz_localize("Europe/Madrid", ambiguous="NaT")[0])   # -> NaT

# Alinear dos series con calendarios distintos NO las rellena: deja solo lo comun.
a = pd.Series([1.0, 2.0, 3.0],
              index=pd.to_datetime(["2024-07-01", "2024-07-02", "2024-07-03"]))
b = pd.Series([10.0, 30.0], index=pd.to_datetime(["2024-07-01", "2024-07-03"]))
print(a.align(b, join="inner")[0].tolist())          # -> [1.0, 3.0]
print(a.reindex(b.index).tolist())                   # -> [1.0, 3.0]
