# Medidas no aditivas: el margen no se suma, se recalcula sobre los totales
LINEAS = [
    {"producto": "teclado", "ingreso": 59.90, "coste": 36.00},
    {"producto": "raton", "ingreso": 12.50, "coste": 6.00},
    {"producto": "monitor", "ingreso": 179.00, "coste": 140.00},
    {"producto": "teclado", "ingreso": 29.95, "coste": 18.00},
]

suma_de_margenes = sum((l["ingreso"] - l["coste"]) / l["ingreso"] for l in LINEAS)
ingreso_total = sum(l["ingreso"] for l in LINEAS)
coste_total = sum(l["coste"] for l in LINEAS)

print("suma de margenes fila a fila:", round(suma_de_margenes, 3))
print("margen real                 :", round((ingreso_total - coste_total) / ingreso_total, 3))
print("ingreso total:", round(ingreso_total, 2), "coste total:", round(coste_total, 2))
# -> suma de margenes fila a fila: 1.536
# -> margen real                 : 0.289
# -> ingreso total: 281.35 coste total: 200.0
# Ese 1.536 es la suma de cuatro porcentajes, no el margen de nada: el margen real es 0.289.
