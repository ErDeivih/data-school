import pandas as pd

# Rebalanceo el dia 1 de cada mes: lo que el motor ajusta al calendario de sesiones.
for primero in pd.date_range("2024-01-01", periods=6, freq="MS"):
    sesion = pd.bdate_range(primero, periods=1)[0]      # primer dia laborable del mes
    aviso = "  (el dia 1 cae en fin de semana)" if sesion != primero else ""
    print(f"{primero:%Y-%m-%d} -> sesion {sesion:%Y-%m-%d}{aviso}")
# -> 2024-01-01 -> sesion 2024-01-01
# -> 2024-02-01 -> sesion 2024-02-01
# -> 2024-03-01 -> sesion 2024-03-01
# -> 2024-04-01 -> sesion 2024-04-01
# -> 2024-05-01 -> sesion 2024-05-01
# -> 2024-06-01 -> sesion 2024-06-03  (el dia 1 cae en fin de semana)
