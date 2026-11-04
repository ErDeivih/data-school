import json

import pandas as pd

crudo = """
[
  {"sensor": "S1", "lecturas": [{"hora": "08:00", "temp": 19.5}, {"hora": "09:00", "temp": 21.0}]},
  {"sensor": "S2", "lecturas": [{"hora": "08:00", "temp": 22.4}]}
]
"""
datos = json.loads(crudo)

# record_path baja a la lista: una fila por lectura, y meta repite el campo del padre
tabla = pd.json_normalize(datos, record_path="lecturas", meta="sensor")
print(tabla.to_string(index=False))          # tres filas, con el sensor repetido
print("columnas:", list(tabla.columns))      # -> ['hora', 'temp', 'sensor']

# La media de la tabla NO es la media por sensor: S1 aporta el doble de filas
print("media de la tabla:", round(tabla["temp"].mean(), 2))          # -> 20.97
por_sensor = tabla.groupby("sensor")["temp"].mean()
print("media por sensor:", round(por_sensor.mean(), 2))              # -> 21.32

# Sin record_path, la lista se queda entera dentro de una celda
sin_bajar = pd.json_normalize(datos)
print("sin record_path:", list(sin_bajar.columns))                   # -> ['sensor', 'lecturas']
