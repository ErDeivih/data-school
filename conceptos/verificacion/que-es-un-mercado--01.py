# El coste de operar: comision con minimo y diferencia de precios, en una ida y vuelta.
nominal_compra = 200 * 24.50
nominal_venta = 200 * 25.10

def comision(nominal, porcentaje=0.001, minimo=3.0):
    """La tarifa del broker: un porcentaje, pero nunca menos que el minimo."""
    return max(nominal * porcentaje, minimo)

c_compra = comision(nominal_compra)
c_venta = comision(nominal_venta)
bruto = nominal_venta - nominal_compra

print("nominal compra :", round(nominal_compra, 2))   # -> 4900.0
print("comision compra:", round(c_compra, 2))         # -> 4.9
print("comision venta :", round(c_venta, 2))          # -> 5.02
print("beneficio bruto:", round(bruto, 2))            # -> 120.0
print("beneficio neto :", round(bruto - c_compra - c_venta, 2))   # -> 110.08
print("coste sobre bruto:", round((c_compra + c_venta) / bruto * 100, 1), "%")   # -> 8.3 %
