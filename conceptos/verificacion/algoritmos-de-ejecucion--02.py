# Cuanto cuesta la prisa: el mismo pedido contra dos libros distintos
# Cada libro es una lista de (precio, acciones disponibles); hay que comprar 1.000.
libro_con_prisa = [(100.00, 400), (100.02, 400), (100.05, 500), (100.10, 800)]
libro_paciente = [(100.00, 800), (100.02, 200), (100.05, 500), (100.10, 800)]
pedido = 1_000

def coste_medio(libro):
    """Precio medio de comprar `pedido` acciones agotando niveles del libro."""
    resta, gastado, compradas = pedido, 0.0, 0
    for precio, tamano in libro:
        toma = min(resta, tamano)
        gastado += toma * precio
        compradas += toma
        resta -= toma
    return gastado / compradas, compradas

prisa, n1 = coste_medio(libro_con_prisa)
paciente, n2 = coste_medio(libro_paciente)

print(f"con prisa: {n1} acciones a {prisa:.4f} EUR")
# -> con prisa: 1000 acciones a 100.0180 EUR
print(f"paciente:  {n2} acciones a {paciente:.4f} EUR")
# -> paciente:  1000 acciones a 100.0040 EUR
print(f"diferencia: {(prisa - paciente) * pedido:.2f} EUR en 1.000 acciones")
# -> diferencia: 14.00 EUR en 1.000 acciones
