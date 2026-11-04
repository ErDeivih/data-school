import pandas as pd

# Mascara condicional: solo se tapa lo que supera el umbral.
ventas = pd.DataFrame({
    "cliente": ["ACME", "PEREZ SL", "GARCIA", "LUNA"],
    "importe": [4200, 300, 800, 1500],
})
vista = ventas.assign(importe=ventas["importe"].where(ventas["importe"] <= 1000, "***"))
print("importes que ve el visitante:", list(vista["importe"]))
# -> ['***', 300, 800, '***']
print("celdas tapadas:", int((vista["importe"] == "***").sum()))
# -> 2

# El numero de celdas tapadas publica el umbral de la politica, y repitiendo la consulta
# con otros filtros se acota el valor exacto por biseccion. La mascara no puede depender
# del valor que esconde.
