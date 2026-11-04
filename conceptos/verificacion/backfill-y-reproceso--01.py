from datetime import date, timedelta

# Un bug activo del 1 de enero al 30 de junio de 2024: lo ya calculado esta mal.
bug_desde, bug_hasta = date(2024, 1, 1), date(2024, 6, 30)
hoy = date(2024, 7, 12)

def rango(a, b):
    """Todas las fechas de a a b, ambas incluidas."""
    return {a + timedelta(days=i) for i in range((b - a).days + 1)}

# Particiones que no existen porque el pipeline estuvo caido del 1 al 3 de julio.
caidas = {date(2024, 7, d) for d in (1, 2, 3)}

reproceso = rango(bug_desde, bug_hasta)      # existen, pero estan mal: hay que reemplazarlas
backfill = {p for p in caidas if p <= hoy}   # no existen: hay que crearlas
particiones_totales = 185                    # dato del enunciado, no se deduce del conjunto
print(f"a reprocesar {len(reproceso)}")                            # -> a reprocesar 182
print(f"a rellenar  {len(backfill)}")                              # -> a rellenar  3
print(f"huecos tras el arreglo {len(reproceso | backfill) - particiones_totales}")  # -> 0

# Y la capa derivada obliga a repetir el trabajo entero otra vez.
print(f"ejecuciones totales {2 * len(reproceso) + len(backfill)}")  # -> 367
