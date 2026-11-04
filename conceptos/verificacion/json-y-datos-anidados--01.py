import json

crudo = """
[
  {"sensor": "S1", "lecturas": [{"hora": "08:00", "temp": 19.5}, {"hora": "09:00", "temp": 21.0}]},
  {"sensor": "S2", "lecturas": [{"hora": "08:00", "temp": 22.4}]}
]
"""
datos = json.loads(crudo)        # texto -> listas y diccionarios de Python
print(type(datos).__name__, len(datos))          # -> list 2
print(datos[0]["sensor"])                        # -> S1
print(datos[0]["lecturas"][1]["temp"])           # -> 21.0
print(datos[1]["lecturas"][0]["hora"])           # -> 08:00
print("total de lecturas:", sum(len(r["lecturas"]) for r in datos))   # -> 3
