# Comprobar que el resultado no cambia es la red de seguridad de cualquier refactor.
def total_viejo(lineas):
    total = 0
    for linea in lineas:
        # Cada linea es un diccionario: se suma precio por cantidad, no los dos campos.
        total = total + linea["precio"] * linea["cantidad"]
    if total > 100:
        total = total * 0.95        # el estricto importa: 100,00 exactos NO llevan descuento
    return round(total, 2)

def total_nuevo(lineas):
    # Expresion generadora dentro de sum: recorre y multiplica sin crear una lista en medio.
    bruto = sum(linea["precio"] * linea["cantidad"] for linea in lineas)
    # Condicional en linea (A if condicion else B): el descuento tiene nombre, bruto.
    return round(bruto * 0.95 if bruto > 100 else bruto, 2)

facturas = [
    [{"precio": 10.0, "cantidad": 3}],
    [{"precio": 25.5, "cantidad": 4}, {"precio": 0.9, "cantidad": 2}],
    [{"precio": 100.0, "cantidad": 1}],
]
# enumerate con start=1 numera las facturas desde 1: el mensaje de error habla de la 1, no de la 0.
for numero, factura in enumerate(facturas, start=1):
    viejo, nuevo = total_viejo(factura), total_nuevo(factura)
    assert viejo == nuevo, f"el refactor cambio el resultado en la factura {numero}"
    print(f"factura {numero}: {viejo:.2f}")

# all() sobre un generador: True si las dos versiones coinciden en todas las facturas.
identicos = all(total_viejo(f) == total_nuevo(f) for f in facturas)
print("resultados identicos:", identicos)          # -> True
