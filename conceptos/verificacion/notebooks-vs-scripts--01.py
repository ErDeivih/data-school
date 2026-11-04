# Detector de estado oculto: compara el orden real de ejecucion con el orden del fichero.
celdas = [
    {"nombre": "cargar_ventas()", "execution_count": 3},
    {"nombre": "ventas = cargar_ventas()", "execution_count": 1},
    {"nombre": "print(ventas.head())", "execution_count": 2},
]

contadores = [c["execution_count"] for c in celdas]
escritas = [c["nombre"] for c in sorted(celdas, key=lambda c: c["execution_count"])]

print("celdas ejecutadas:", len(contadores))
print("contadores en orden creciente:", contadores == sorted(contadores))
print("empieza el fichero por:", celdas[0]["nombre"])
print("pero se ejecuto primero:", escritas[0])
print("celdas fuera de sitio:", sum(1 for i, c in enumerate(contadores) if c != i + 1))
