# Precio fijo: la tarifa que cobras de verdad baja con cada hora extra.
estimacion_horas = 120
precio_cerrado = 12000       # sale a 100 EUR/h si el alcance no se mueve
objetivo = 80                # por debajo de esto el proyecto no compensa

print(f"tarifa con el alcance previsto {precio_cerrado / estimacion_horas:.2f} EUR/h")  # -> 100.00 EUR/h
print(f"horas maximas antes del limite {precio_cerrado / objetivo:.0f} h")             # -> 150 h
for h in (120, 138, 154, 190):
    # 154 h son las del ejemplo: dos rondas de cambios sobre la estimacion
    print(f"  {h:>3} h facturadas  tarifa real {precio_cerrado / h:>6.2f} EUR/h")
