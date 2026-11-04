import pandas as pd

# Los 6 pedidos tal como salen del sistema transaccional.
crudo = pd.DataFrame({
    "pedido_id": [1, 2, 3, 4, 5, 6],
    "cliente_id": [10, 11, 10, 12, 13, 12],
    "importe": [25.0, -3.0, 40.0, 15.0, None, 60.0],
    "estado": ["pagado", "pagado", "devuelto", "pagado", "pagado", "pagado"],
})

# La regla de negocio, escrita una sola vez.
valido = crudo[(crudo["estado"] == "pagado") & (crudo["importe"] > 0)]

# ETL: al almacen solo llega el agregado.
etl = valido.groupby("cliente_id")["importe"].sum()
print("ETL filas cargadas:", len(etl))                # -> ETL filas cargadas: 2
print("ETL total:", float(etl.sum()))                 # -> ETL total: 100.0

# ELT: al almacen llega todo el crudo y la regla se aplica despues.
print("ELT filas cargadas:", len(crudo))              # -> ELT filas cargadas: 6
print("ELT total:", float(valido["importe"].sum()))   # -> ELT total: 100.0
print("Filas descartadas:", len(crudo) - len(valido)) # -> Filas descartadas: 3
