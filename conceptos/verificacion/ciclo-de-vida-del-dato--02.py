# El ciclo de vida como datos: dueño, clasificacion y plazo por conjunto
REGISTRO = [
    {"conjunto": "pedidos", "dueno": "equipo-ventas", "clasificacion": "personal", "retencion_dias": 1825},
    {"conjunto": "ventas_diarias", "dueno": "equipo-datos", "clasificacion": "interno", "retencion_dias": 3650},
    {"conjunto": "clics_web", "dueno": "equipo-marketing", "clasificacion": "personal", "retencion_dias": 400},
    {"conjunto": "catalogo", "dueno": "equipo-catalogo", "clasificacion": "publico", "retencion_dias": 3650},
]

# Regla de revision: todo conjunto con datos personales debe caducar en menos de 3 anios
LIMITE_PERSONAL = 1095
revisar = [c["conjunto"] for c in REGISTRO
           if c["clasificacion"] == "personal" and c["retencion_dias"] > LIMITE_PERSONAL]

print("conjuntos con datos personales a revisar:", len(revisar))   # -> 1
print("el que se pasa:", revisar[0])                              # -> pedidos
print("sin dueno:", sum(1 for c in REGISTRO if not c["dueno"].strip()))   # -> 0

media = sum(c["retencion_dias"] for c in REGISTRO) / len(REGISTRO)
print("retencion media en anios:", round(media / 365, 1))          # -> 6.5
