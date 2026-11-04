import pandas as pd

origen = pd.DataFrame({
    "id": range(1, 8),
    "importe": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0],
    "fecha": ["2024-03-29", "2024-03-29", "2024-03-30", "2024-03-30", "2024-03-30",
              "2024-03-31", "2024-03-31"],
})
# El destino perdio las dos filas del 31: un filtro de fecha con la zona horaria mal puesta
destino = origen[origen.fecha != "2024-03-31"].copy()

filas = len(origen) - len(destino)
euros = origen.importe.sum() - destino.importe.sum()
print(f"faltan {filas} filas y {euros:.2f} euros")                        # -> faltan 2 filas y 130.00 euros
print(f"relativo en filas: {100 * filas / len(origen):.1f} %")           # -> relativo en filas: 28.6 %
print("ids que no llegaron:", sorted(set(origen.id) - set(destino.id)))   # -> ids que no llegaron: [6, 7]
