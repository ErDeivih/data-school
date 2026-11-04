# Margen y liquidez forzosa: cuando el broker compra por ti
precio_venta = 50.0
acciones = 100
garantia = 0.50 * precio_venta * acciones   # el 50 % del valor, como pide la Regulacion T
mantenimiento = 0.30                        # margen exigido sobre el valor actual

print(f"garantia aportada: {garantia:.2f} EUR")
# -> garantia aportada: 2500.00 EUR
for precio in (50.0, 60.0, 65.0):
    equity = garantia + precio_venta * acciones - precio * acciones
    exigido = mantenimiento * precio * acciones
    estado = "ok" if equity >= exigido else "MARGIN CALL"
    print(f"precio {precio:>5.2f}: equity {equity:>8.2f} EUR, exigido {exigido:>8.2f} EUR -> {estado}")
# -> precio 50.00: equity  2500.00 EUR, exigido  1500.00 EUR -> ok
# -> precio 60.00: equity  1500.00 EUR, exigido  1800.00 EUR -> MARGIN CALL
# -> precio 65.00: equity  1000.00 EUR, exigido  1950.00 EUR -> MARGIN CALL
