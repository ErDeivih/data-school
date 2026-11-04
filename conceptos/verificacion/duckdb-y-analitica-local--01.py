import duckdb
import pandas as pd

ventas = pd.DataFrame({
    "region": ["norte", "sur", "norte", "sur", "norte"],
    "fecha": pd.to_datetime(["2024-03-01", "2024-03-05", "2024-04-02",
                             "2024-04-02", "2024-05-03"]),
    "importe": [120.0, 80.0, 200.0, 50.0, 30.0],
})

con = duckdb.connect()          # en memoria: ni servidor ni fichero
con.register("ventas", ventas)  # consulta el DataFrame sin copiarlo

filas = con.sql("""
    SELECT region, SUM(importe) AS total
    FROM ventas
    WHERE fecha >= DATE '2024-04-01'
    GROUP BY region
    ORDER BY total DESC
""").fetchall()

print("grupos devueltos:", len(filas))       # -> grupos devueltos: 2
print("primera region:", filas[0][0])        # -> primera region: norte
print("total de la primera:", filas[0][1])   # -> total de la primera: 230.0
print("total de la segunda:", filas[1][1])   # -> total de la segunda: 50.0
